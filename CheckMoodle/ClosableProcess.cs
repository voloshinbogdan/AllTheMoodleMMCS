using System.Diagnostics;


namespace CheckMoodle
{
    class ClosableProcess
    {
        public Process p { get; }
        public ClosableProcess(Process p)
        {
            this.p = p;
        }

        ~ClosableProcess()
        {
            if (!p.HasExited)
                p.Kill();
            p.Close();
        }
    }
}
