using System.Windows;
using System.Windows.Controls;
using System.Windows.Media.Animation;

namespace Orion.Views
{
    /// <summary>
    /// Interaction logic for CognitiveCoreView.xaml
    /// </summary>
    public partial class CognitiveCoreView : UserControl
    {
        public CognitiveCoreView()
        {
            InitializeComponent();

            Loaded += CognitiveCoreView_Loaded;
        }

        private void CognitiveCoreView_Loaded(object sender, RoutedEventArgs e)
        {
            var pulse = (Storyboard)FindResource("CorePulse");
            pulse.Begin();
        }
    }
}
