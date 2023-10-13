using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Threading;
using System.IO;
using Newtonsoft.Json;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;   

namespace CheckMoodle
{
    public partial class Form1 : Form
    {

        // WIN32
        [DllImport("user32.dll", SetLastError = true)]
        static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);

        private const int SW_SHOWMAXIMIZED = 3;
        private const int SW_SHOWMINIMIZED = 3;

        private const uint WM_SYSCOMMAND = 0x0112;

        [DllImport("user32.dll")]
        static extern IntPtr SetParent(IntPtr hWndChild, IntPtr hWndNewParent);
        [DllImport("user32.dll")]
        static extern bool PostMessage(IntPtr hWnd, uint Msg, uint wParam, uint lParam);
        // <-WIN32

        IIDE IDE;
        IWebDriver webdriver;
        private ClosableProcess _processWebdriver;
        private Process _processChrome;

        List<string> Args;
        string html;
        string mossURL;
        int prevSubInd = -1;
        private double max_score = -1;

        const int GWL_STYLE = -16;
        const int WS_BORDER = 0x0080000;
        const int WS_CAPTION = 0x00C0000;

        [DllImport("user32.dll", SetLastError = true)]
        public static extern int GetWindowLong(IntPtr hWnd, int nIndex);

        [DllImport("user32.dll")]
        public static extern int SetWindowLong(IntPtr hWnd, int nIndex, int dwNewLong);

        public static void MakeProcessWindowBorderless(Process process)
        {
            if (process != null)
            {
                IntPtr hwnd = process.MainWindowHandle;
                int style = GetWindowLong(hwnd, GWL_STYLE);
                SetWindowLong(hwnd, GWL_STYLE, (style & ~WS_BORDER & ~WS_CAPTION));
            }
        }

        // Table variables
        private int minColumnWidthComment = -1;
        private int minRawHeight = -1;

        public Form1()
        {
            InitializeComponent();
        }

        public Form1(string[] args)
        {
            InitializeComponent();
            
            // Table Setup
            dataGridView1.Columns["TaskComment"].DefaultCellStyle.WrapMode = DataGridViewTriState.True;
            minColumnWidthComment = dataGridView1.Columns["TaskComment"].Width;
            minRawHeight = dataGridView1.RowTemplate.Height;


            string working_dir = "";
            string ide_code = "";
            if (args.Length == 1)
            {
                working_dir = args[0];
                string cfg_path = Path.Combine(working_dir, "assign.json");
                if (File.Exists(cfg_path))
                {
                    var cfgt = File.ReadAllText(cfg_path);
                    dynamic cfg = JsonConvert.DeserializeObject(cfgt);
                    ide_code = cfg.IDE;
                    max_score = cfg.max_score;
                }
            }
            else if (args.Length == 3)
            {
                working_dir = args[0];
                ide_code = args[1];
                max_score = double.Parse(args[2].Replace('.', ','));
            }
            else
                throw new ArgumentException("Should be 3 parameters (path to folder, IDE, max score) or 1 (path to folder but with json");

            maxScL.Text = "/" + max_score;
            html = Path.Combine(working_dir, "task.html");

            var t = File.ReadAllText("config.json");
            dynamic config = JsonConvert.DeserializeObject(t);
            Args = Directory.GetDirectories(working_dir).Where(s => s.Contains("assignsubmission_file")).ToList();
            Submissions.Items.AddRange(Args.Select(s => new DirectoryInfo(s).Name).ToArray());

            switch (ide_code)
            {
                case "vsc":
                    IDE = new OpenCloseIDE((string)config.vscode, "-n", p =>
                    {
                        IDEResize(p);
                        if (Submissions.SelectedIndex == -1)
                            this.Text = "Checker";
                        else
                            this.Text = new DirectoryInfo(working_dir).Name + "\\" +
                                new DirectoryInfo(Args[Submissions.SelectedIndex]).Name + " - Checker";
                    });
                    break;
                case "vs":
                    IDE = new VSAPI((string)config.vsversion, @".", p =>
                    {
                        IDEResize(p);
                        if (Submissions.SelectedIndex == -1)
                            this.Text = "Checker";
                        else
                            this.Text = new DirectoryInfo(working_dir).Name + "\\" +
                                 new DirectoryInfo(Args[Submissions.SelectedIndex]).Name + " - Checker";
                    });
                    break;
                case "pas":
                    IDE = new OpenCloseIDE((string)config.pascal, "", p =>
                    {
                        Thread.Sleep(100);
                        IDEResize(p);
                        if (Submissions.SelectedIndex == -1)
                            this.Text = "Checker";
                        else
                            this.Text = new DirectoryInfo(working_dir).Name + "\\" +
                                new DirectoryInfo(Args[Submissions.SelectedIndex]).Name + " - Checker";
                    },
                    s =>
                    {
                        string res = "";
                        foreach (var f in Directory.GetFiles(s, "*.*", SearchOption.AllDirectories))
                        {
                            if (Path.GetExtension(f) == ".pas")
                                res += "\"" + f + "\" ";
                        }
                        return res;
                    }
                    );
                    break;
                default:
                    throw new ArgumentException("No such IDE " + ide_code);

            }

            {

                var cService = ChromeDriverService.CreateDefaultService();
                cService.HideCommandPromptWindow = true;

                var options = new ChromeOptions();
                options.AddExcludedArgument("enable-automation");

                options.AddArgument("--window-position=-32000,-32000");
                webdriver = new ChromeDriver(cService, options);
                webdriver.Url = html.Replace("#", "%23");
                
                while (string.IsNullOrEmpty(webdriver.CurrentWindowHandle))
                {
                    Thread.Sleep(100);
                }
                string title = "task.html - Google Chrome";
                _processWebdriver = new ClosableProcess(Process.GetProcessesByName("chromedriver").FirstOrDefault());
                _processChrome = Process.GetProcesses()
                    .FirstOrDefault(x => x.MainWindowTitle == title);
                SetParent(_processChrome.MainWindowHandle, panel2.Handle);
                MakeProcessWindowBorderless(_processChrome);
                panel2_Resize(null, null);

            }
            Submissions.SelectedIndex = 0;
        }

        private void button1_Click(object sender, EventArgs e) //+
        {
            Submissions.SelectedIndex = (Submissions.SelectedIndex + 1) % Args.Count;
        }
        private void panel2_Resize(object sender, EventArgs e)
        {
            if (_processChrome.MainWindowHandle != null)
                MoveWindow(_processChrome.MainWindowHandle, 0, -50, panel2.Width, panel2.Height + 50, true);
        }

        private void back_Click(object sender, EventArgs e)  //+
        {
            Submissions.SelectedIndex = (Args.Count + Submissions.SelectedIndex - 1) % Args.Count;
        }

        private void Submissions_SelectedIndexChanged(object sender, EventArgs e) //+
        {
            this.Enabled = false;
            if (prevSubInd != -1)
                SaveScore(prevSubInd);
            IDE.Show(Args[Submissions.SelectedIndex]);
            string t;
            var moss_path = Path.Combine(Args[Submissions.SelectedIndex], "moss.json");
            if (File.Exists(moss_path))
            {
                addMoss.Enabled = true;
                t = File.ReadAllText(moss_path);
                dynamic m = JsonConvert.DeserializeObject(t);
                moss.Text = m.percent;
                mossURL = m.url;
            }
            else
            {
                addMoss.Enabled = false;
                moss.Text = "";
                mossURL = null;
            }
            // Load task if exists
            var pdf = Directory.GetFiles(Args[Submissions.SelectedIndex], "*.pdf", SearchOption.AllDirectories).FirstOrDefault();
            if (pdf != null)
                webdriver.Url = pdf.Replace("#", "%23");

            // Load Score
            string score_path = Path.Combine(Args[Submissions.SelectedIndex], "score.json");
            score.Text = "";
            comment.Text = "";
            if (File.Exists(score_path))
            {
                t = File.ReadAllText(score_path);
                dynamic s = JsonConvert.DeserializeObject(t);
                score.Text = s.score;
                comment.Text = s.comment;
            }
            prevSubInd = Submissions.SelectedIndex;
            this.Enabled = true;
        }

        private void SaveB_Click(object sender, EventArgs e) //+
        {
            SaveScore(Submissions.SelectedIndex);
        }

        private void SaveScore(int ind) 
        {
            if (score.Text == "" && comment.Text == "")
                return;
            File.WriteAllText(Path.Combine(Args[ind], "score.json"),
@"{
    ""score"": " + score.Text.Replace(',', '.') + @",
    ""comment"": """ + comment.Text.Replace(@"\", @"\\").Replace("\n", "\\n").Replace("\t", "\\t") + @"""
}");
        }

        private void score_Validating(object sender, CancelEventArgs e) //+
        {
            double r;
            if (score.Text == "" || double.TryParse(score.Text.Replace(".", ","), out r) && r >= 0 && r <= max_score)
                return;

            e.Cancel = true;
            scoreError.SetError(score, "Shoould be real number R(0 <= R <= " + max_score + ")");
            
        }

        private void score_Validated(object sender, EventArgs e) //+
        {
            scoreError.SetError(score, "");
        }

        private void addMoss_Click(object sender, EventArgs e) //+
        {
            comment.Text = string.Format("Процент плагиата: {0}({1})\n", moss.Text, mossURL) + comment.Text;
        }

        private void moss_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e) //+
        {
            if (mossURL != null)
                Process.Start(mossURL);
        }

        private void Form1_FormClosed(object sender, FormClosedEventArgs e)
        {
            try
            {
                IDE.Quit();

            }
            catch (Exception)
            {
            }

            try
            {
                webdriver.Quit();

            }
            catch (Exception)
            {

            }

            try
            {
                webdriver.Dispose();

            }
            catch (Exception)
            {

            }
        }

        private void Form1_Resize(object sender, EventArgs e)
        {
            if (WindowState == FormWindowState.Maximized)
            {
                WindowState = FormWindowState.Normal;
                Top = Screen.PrimaryScreen.WorkingArea.Top;
                Left = 2 * Screen.PrimaryScreen.WorkingArea.Width / 3;
                Width = Screen.PrimaryScreen.WorkingArea.Width - Left;
                Height = Screen.PrimaryScreen.WorkingArea.Height;
            }
            IDEResize(IDE?.GetProcess());

        }

        private void IDEResize(Process p)
        {
            if (p?.MainWindowHandle != null)
                MoveWindow(p.MainWindowHandle, 0, this.Top, this.Left + 20, this.Height, true);
        }

        private void Form1_Move(object sender, EventArgs e)
        {
            IDEResize(IDE?.GetProcess());
        }

        private void Rtb_AdjustRowSize(object sender, EventArgs e)
        {
            RichTextBox rtb = sender as RichTextBox;
            if (rtb != null && dataGridView1.CurrentCell != null)
            {
                using (Graphics graphics = dataGridView1.CreateGraphics())
                {
                    SizeF size = graphics.MeasureString(rtb.Text, dataGridView1.Font);
                    dataGridView1.Rows[dataGridView1.CurrentCell.RowIndex].Height = Math.Max((int)(size.Height * 1.05) + 5, minRawHeight);
                    dataGridView1.Columns[dataGridView1.CurrentCell.ColumnIndex].Width = Math.Max((int)size.Width + 5, minColumnWidthComment);
                }
            }
        }

        private void dataGridView_CellBeginEdit(object sender, DataGridViewEditingControlShowingEventArgs e)
        {
            if (dataGridView1.CurrentCell.ColumnIndex == dataGridView1.Columns["TaskComment"].Index &&
                e.Control is DataGridViewRichTextBoxEditingControl)
            {
                DataGridViewRichTextBoxEditingControl rtb = e.Control as DataGridViewRichTextBoxEditingControl;
                rtb.AdjustRowHeight += Rtb_AdjustRowSize;
            }

        }

        private void dataGridView1_CellEndEdit(object sender, DataGridViewCellEventArgs e)
        {
            if (e.ColumnIndex == dataGridView1.Columns["TaskComment"].Index &&
                dataGridView1.EditingControl is DataGridViewRichTextBoxEditingControl)
            {
                DataGridViewRichTextBoxEditingControl rtb = dataGridView1.EditingControl as DataGridViewRichTextBoxEditingControl;
                rtb.AdjustRowHeight -= Rtb_AdjustRowSize;
            }
        }
    }
}
