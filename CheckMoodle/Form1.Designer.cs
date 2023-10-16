using CSharpFileExplorer;

namespace CheckMoodle
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.loadIDE = new System.Windows.Forms.Timer(this.components);
            this.scoreError = new System.Windows.Forms.ErrorProvider(this.components);
            this.splitContainer2 = new System.Windows.Forms.SplitContainer();
            this.panel2 = new System.Windows.Forms.Panel();
            this.splitContainer3 = new System.Windows.Forms.SplitContainer();
            this.justifyScores = new System.Windows.Forms.Button();
            this.generateFromTable = new System.Windows.Forms.Button();
            this.dataGridView1 = new System.Windows.Forms.DataGridView();
            this.Perfect = new System.Windows.Forms.DataGridViewCheckBoxColumn();
            this.TaskName = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.TaskScore = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.MaxScore = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.TaskComment = new CheckMoodle.DataGridViewRichTextBoxColumn();
            this.maxScL = new System.Windows.Forms.Label();
            this.addMoss = new System.Windows.Forms.Button();
            this.moss = new System.Windows.Forms.LinkLabel();
            this.SaveB = new System.Windows.Forms.Button();
            this.score = new System.Windows.Forms.TextBox();
            this.comment = new System.Windows.Forms.RichTextBox();
            this.Submissions = new System.Windows.Forms.ComboBox();
            this.Save = new System.Windows.Forms.Button();
            this.back = new System.Windows.Forms.Button();
            this.fileSystemWatcher1 = new System.IO.FileSystemWatcher();
            this.dataGridViewRichTextBoxColumn1 = new CheckMoodle.DataGridViewRichTextBoxColumn();
            this.cellError = new System.Windows.Forms.ErrorProvider(this.components);
            this.rowError = new System.Windows.Forms.ErrorProvider(this.components);
            this.tableToCommentError = new System.Windows.Forms.ErrorProvider(this.components);
            ((System.ComponentModel.ISupportInitialize)(this.scoreError)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer2)).BeginInit();
            this.splitContainer2.Panel1.SuspendLayout();
            this.splitContainer2.Panel2.SuspendLayout();
            this.splitContainer2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer3)).BeginInit();
            this.splitContainer3.Panel1.SuspendLayout();
            this.splitContainer3.Panel2.SuspendLayout();
            this.splitContainer3.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.fileSystemWatcher1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.cellError)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.rowError)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.tableToCommentError)).BeginInit();
            this.SuspendLayout();
            // 
            // scoreError
            // 
            this.scoreError.ContainerControl = this;
            // 
            // splitContainer2
            // 
            this.splitContainer2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitContainer2.Location = new System.Drawing.Point(0, 0);
            this.splitContainer2.Name = "splitContainer2";
            this.splitContainer2.Orientation = System.Windows.Forms.Orientation.Horizontal;
            // 
            // splitContainer2.Panel1
            // 
            this.splitContainer2.Panel1.Controls.Add(this.panel2);
            // 
            // splitContainer2.Panel2
            // 
            this.splitContainer2.Panel2.Controls.Add(this.splitContainer3);
            this.splitContainer2.Size = new System.Drawing.Size(534, 553);
            this.splitContainer2.SplitterDistance = 382;
            this.splitContainer2.TabIndex = 14;
            // 
            // panel2
            // 
            this.panel2.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.panel2.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.panel2.Location = new System.Drawing.Point(3, 3);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(528, 377);
            this.panel2.TabIndex = 6;
            this.panel2.Resize += new System.EventHandler(this.panel2_Resize);
            // 
            // splitContainer3
            // 
            this.splitContainer3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitContainer3.Location = new System.Drawing.Point(0, 0);
            this.splitContainer3.Name = "splitContainer3";
            // 
            // splitContainer3.Panel1
            // 
            this.splitContainer3.Panel1.Controls.Add(this.justifyScores);
            this.splitContainer3.Panel1.Controls.Add(this.generateFromTable);
            this.splitContainer3.Panel1.Controls.Add(this.dataGridView1);
            // 
            // splitContainer3.Panel2
            // 
            this.splitContainer3.Panel2.Controls.Add(this.maxScL);
            this.splitContainer3.Panel2.Controls.Add(this.addMoss);
            this.splitContainer3.Panel2.Controls.Add(this.moss);
            this.splitContainer3.Panel2.Controls.Add(this.SaveB);
            this.splitContainer3.Panel2.Controls.Add(this.score);
            this.splitContainer3.Panel2.Controls.Add(this.comment);
            this.splitContainer3.Panel2.Controls.Add(this.Submissions);
            this.splitContainer3.Panel2.Controls.Add(this.Save);
            this.splitContainer3.Panel2.Controls.Add(this.back);
            this.splitContainer3.Size = new System.Drawing.Size(534, 167);
            this.splitContainer3.SplitterDistance = 266;
            this.splitContainer3.TabIndex = 0;
            // 
            // justifyScores
            // 
            this.justifyScores.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.justifyScores.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.justifyScores.Location = new System.Drawing.Point(223, 58);
            this.justifyScores.Name = "justifyScores";
            this.justifyScores.Size = new System.Drawing.Size(39, 23);
            this.justifyScores.TabIndex = 2;
            this.justifyScores.Text = "≡";
            this.justifyScores.UseVisualStyleBackColor = true;
            this.justifyScores.Click += new System.EventHandler(this.justifyScores_Click);
            // 
            // generateFromTable
            // 
            this.generateFromTable.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.generateFromTable.Font = new System.Drawing.Font("Microsoft Sans Serif", 18F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.generateFromTable.Location = new System.Drawing.Point(222, 11);
            this.generateFromTable.Name = "generateFromTable";
            this.generateFromTable.Size = new System.Drawing.Size(29, 40);
            this.generateFromTable.TabIndex = 1;
            this.generateFromTable.Text = "✍️";
            this.generateFromTable.UseVisualStyleBackColor = true;
            this.generateFromTable.Click += new System.EventHandler(this.generateFromTable_Click);
            // 
            // dataGridView1
            // 
            this.dataGridView1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.dataGridView1.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView1.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.Perfect,
            this.TaskName,
            this.TaskScore,
            this.MaxScore,
            this.TaskComment});
            this.dataGridView1.Location = new System.Drawing.Point(13, 11);
            this.dataGridView1.Name = "dataGridView1";
            this.dataGridView1.RowHeadersWidth = 25;
            this.dataGridView1.Size = new System.Drawing.Size(203, 150);
            this.dataGridView1.TabIndex = 0;
            this.dataGridView1.CellEndEdit += new System.Windows.Forms.DataGridViewCellEventHandler(this.dataGridView1_CellEndEdit);
            this.dataGridView1.CellValidated += new System.Windows.Forms.DataGridViewCellEventHandler(this.dataGridView1_CellValidated);
            this.dataGridView1.CellValidating += new System.Windows.Forms.DataGridViewCellValidatingEventHandler(this.dataGridView1_CellValidating);
            this.dataGridView1.CellValueChanged += new System.Windows.Forms.DataGridViewCellEventHandler(this.dataGridView1_CellValueChanged);
            this.dataGridView1.EditingControlShowing += new System.Windows.Forms.DataGridViewEditingControlShowingEventHandler(this.dataGridView_CellBeginEdit);
            this.dataGridView1.RowLeave += new System.Windows.Forms.DataGridViewCellEventHandler(this.dataGridView1_RowLeave);
            this.dataGridView1.RowValidated += new System.Windows.Forms.DataGridViewCellEventHandler(this.dataGridView1_RowValidated);
            this.dataGridView1.RowValidating += new System.Windows.Forms.DataGridViewCellCancelEventHandler(this.dataGridView1_RowValidating);
            // 
            // Perfect
            // 
            this.Perfect.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.AllCellsExceptHeader;
            this.Perfect.HeaderText = "Perfect";
            this.Perfect.Name = "Perfect";
            this.Perfect.Width = 21;
            // 
            // TaskName
            // 
            this.TaskName.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.AllCellsExceptHeader;
            this.TaskName.HeaderText = "Name";
            this.TaskName.Name = "TaskName";
            this.TaskName.Width = 21;
            // 
            // TaskScore
            // 
            this.TaskScore.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.AllCellsExceptHeader;
            this.TaskScore.HeaderText = "Score";
            this.TaskScore.Name = "TaskScore";
            this.TaskScore.Width = 21;
            // 
            // MaxScore
            // 
            this.MaxScore.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.AllCellsExceptHeader;
            this.MaxScore.HeaderText = "Max Score";
            this.MaxScore.Name = "MaxScore";
            this.MaxScore.Width = 21;
            // 
            // TaskComment
            // 
            this.TaskComment.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.None;
            this.TaskComment.HeaderText = "Comment";
            this.TaskComment.Name = "TaskComment";
            this.TaskComment.Width = 57;
            // 
            // maxScL
            // 
            this.maxScL.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.maxScL.AutoSize = true;
            this.maxScL.Location = new System.Drawing.Point(227, 11);
            this.maxScL.Name = "maxScL";
            this.maxScL.Size = new System.Drawing.Size(0, 13);
            this.maxScL.TabIndex = 13;
            // 
            // addMoss
            // 
            this.addMoss.Location = new System.Drawing.Point(49, 5);
            this.addMoss.Name = "addMoss";
            this.addMoss.Size = new System.Drawing.Size(18, 23);
            this.addMoss.TabIndex = 12;
            this.addMoss.Text = "ᒣ";
            this.addMoss.UseVisualStyleBackColor = true;
            this.addMoss.Click += new System.EventHandler(this.addMoss_Click);
            // 
            // moss
            // 
            this.moss.AutoSize = true;
            this.moss.Location = new System.Drawing.Point(11, 8);
            this.moss.Name = "moss";
            this.moss.Size = new System.Drawing.Size(31, 13);
            this.moss.TabIndex = 7;
            this.moss.TabStop = true;
            this.moss.Text = "moss";
            this.moss.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.moss_LinkClicked);
            // 
            // SaveB
            // 
            this.SaveB.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.SaveB.Location = new System.Drawing.Point(187, 113);
            this.SaveB.Name = "SaveB";
            this.SaveB.Size = new System.Drawing.Size(72, 23);
            this.SaveB.TabIndex = 11;
            this.SaveB.Text = "💾";
            this.SaveB.UseVisualStyleBackColor = true;
            this.SaveB.Click += new System.EventHandler(this.SaveB_Click);
            // 
            // score
            // 
            this.score.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.score.Location = new System.Drawing.Point(176, 7);
            this.score.Name = "score";
            this.score.Size = new System.Drawing.Size(45, 20);
            this.score.TabIndex = 1;
            this.score.Validating += new System.ComponentModel.CancelEventHandler(this.score_Validating);
            this.score.Validated += new System.EventHandler(this.score_Validated);
            // 
            // comment
            // 
            this.comment.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.comment.Location = new System.Drawing.Point(3, 34);
            this.comment.Name = "comment";
            this.comment.Size = new System.Drawing.Size(258, 75);
            this.comment.TabIndex = 2;
            this.comment.Text = "";
            // 
            // Submissions
            // 
            this.Submissions.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.Submissions.FormattingEnabled = true;
            this.Submissions.Location = new System.Drawing.Point(3, 138);
            this.Submissions.Name = "Submissions";
            this.Submissions.Size = new System.Drawing.Size(256, 21);
            this.Submissions.TabIndex = 9;
            this.Submissions.SelectedIndexChanged += new System.EventHandler(this.Submissions_SelectedIndexChanged);
            // 
            // Save
            // 
            this.Save.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.Save.Location = new System.Drawing.Point(124, 113);
            this.Save.Name = "Save";
            this.Save.Size = new System.Drawing.Size(57, 23);
            this.Save.TabIndex = 3;
            this.Save.Text = "►";
            this.Save.UseVisualStyleBackColor = true;
            this.Save.Click += new System.EventHandler(this.button1_Click);
            // 
            // back
            // 
            this.back.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.back.Location = new System.Drawing.Point(62, 113);
            this.back.Name = "back";
            this.back.Size = new System.Drawing.Size(56, 23);
            this.back.TabIndex = 8;
            this.back.Text = "◄";
            this.back.UseVisualStyleBackColor = true;
            this.back.Click += new System.EventHandler(this.back_Click);
            // 
            // fileSystemWatcher1
            // 
            this.fileSystemWatcher1.EnableRaisingEvents = true;
            this.fileSystemWatcher1.SynchronizingObject = this;
            // 
            // dataGridViewRichTextBoxColumn1
            // 
            this.dataGridViewRichTextBoxColumn1.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.AllCells;
            this.dataGridViewRichTextBoxColumn1.HeaderText = "Comment";
            this.dataGridViewRichTextBoxColumn1.Name = "dataGridViewRichTextBoxColumn1";
            // 
            // cellError
            // 
            this.cellError.ContainerControl = this;
            // 
            // rowError
            // 
            this.rowError.ContainerControl = this;
            // 
            // tableToCommentError
            // 
            this.tableToCommentError.ContainerControl = this;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(534, 553);
            this.Controls.Add(this.splitContainer2);
            this.Name = "Form1";
            this.Text = "Form1";
            this.Activated += new System.EventHandler(this.Form1_Activated);
            this.FormClosed += new System.Windows.Forms.FormClosedEventHandler(this.Form1_FormClosed);
            this.Move += new System.EventHandler(this.Form1_Move);
            this.Resize += new System.EventHandler(this.Form1_Resize);
            this.Validating += new System.ComponentModel.CancelEventHandler(this.score_Validating);
            ((System.ComponentModel.ISupportInitialize)(this.scoreError)).EndInit();
            this.splitContainer2.Panel1.ResumeLayout(false);
            this.splitContainer2.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer2)).EndInit();
            this.splitContainer2.ResumeLayout(false);
            this.splitContainer3.Panel1.ResumeLayout(false);
            this.splitContainer3.Panel2.ResumeLayout(false);
            this.splitContainer3.Panel2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer3)).EndInit();
            this.splitContainer3.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.fileSystemWatcher1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.cellError)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.rowError)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.tableToCommentError)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion
        private System.Windows.Forms.Timer loadIDE;
        private System.Windows.Forms.ErrorProvider scoreError;
        private System.Windows.Forms.SplitContainer splitContainer2;
        private System.Windows.Forms.Panel panel2;
        private System.Windows.Forms.SplitContainer splitContainer3;
        private System.Windows.Forms.Label maxScL;
        private System.Windows.Forms.Button addMoss;
        private System.Windows.Forms.LinkLabel moss;
        private System.Windows.Forms.Button SaveB;
        private System.Windows.Forms.TextBox score;
        private System.Windows.Forms.RichTextBox comment;
        private System.Windows.Forms.ComboBox Submissions;
        private System.Windows.Forms.Button Save;
        private System.Windows.Forms.Button back;
        private System.IO.FileSystemWatcher fileSystemWatcher1;
        private System.Windows.Forms.DataGridView dataGridView1;
        private System.Windows.Forms.Button generateFromTable;
        private DataGridViewRichTextBoxColumn dataGridViewRichTextBoxColumn1;
        private System.Windows.Forms.DataGridViewCheckBoxColumn Perfect;
        private System.Windows.Forms.DataGridViewTextBoxColumn TaskName;
        private System.Windows.Forms.DataGridViewTextBoxColumn TaskScore;
        private System.Windows.Forms.DataGridViewTextBoxColumn MaxScore;
        private DataGridViewRichTextBoxColumn TaskComment;
        private System.Windows.Forms.Button justifyScores;
        private System.Windows.Forms.ErrorProvider cellError;
        private System.Windows.Forms.ErrorProvider rowError;
        private System.Windows.Forms.ErrorProvider tableToCommentError;
    }
}

