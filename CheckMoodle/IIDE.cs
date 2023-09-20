using System.Diagnostics;

namespace CheckMoodle
{
    public abstract class IIDE
    {
        public abstract Process GetProcess();
        public abstract void Show(string path);
        public abstract void Quit();
    }
}