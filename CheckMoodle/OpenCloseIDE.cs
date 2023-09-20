using System;
using System.Diagnostics;
using System.Threading;

namespace CheckMoodle
{
    public class OpenCloseIDE : IIDE
    {
        private string IDEName;
        private string RunArgs; 
        private Process IDE;
        private Action<Process> ConfigureApp;
        private Func<string, string> PreprocessParameters;
        public OpenCloseIDE(string IDEName, string RunArgs,
            Action<Process> ConfigureApp = null,
            Func<string, string> PreprocessParameters = null)
        {
            this.IDEName = IDEName;
            this.RunArgs = RunArgs;
            this.ConfigureApp = ConfigureApp;
            if (PreprocessParameters == null)
                this.PreprocessParameters = s => s;
            else
                this.PreprocessParameters = PreprocessParameters;
        }

        public override Process GetProcess()
        {
            return IDE;
        }

        public override void Show(string path)
        {
            if (IDE != null)
            {
                Quit();
            }
            ProcessStartInfo info = new ProcessStartInfo();
            info.FileName = IDEName;
            info.Arguments = RunArgs + " " + PreprocessParameters(path);
            info.UseShellExecute = false;
            IDE = Process.Start(info);
            while (string.IsNullOrEmpty(IDE.MainWindowTitle))
            {
                Thread.Sleep(100);
                IDE.Refresh();
            }
            if (ConfigureApp != null)
                ConfigureApp(IDE);
        }

        public override void Quit()
        {
            if (IDE != null && !IDE.HasExited)
            {
                IDE.Kill();
                IDE.Close();
            }
        }
    }
}