using System;
using System.Windows;
using System.Windows.Media.Animation;

namespace Orion
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            Loaded += MainWindow_Loaded;
        }
        private void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            StartTicker();
            var storyboard = (Storyboard)FindResource("BackgroundAnimation");
            storyboard.Begin();
        }

        private void StartTicker()
        {
            double windowWidth = ActualWidth;
            double tickerWidth = TickerContent.ActualWidth;

            var animation = new DoubleAnimation
            {
                From = windowWidth,
                To = -tickerWidth,
                Duration = TimeSpan.FromSeconds(22),
                RepeatBehavior = RepeatBehavior.Forever
            };

            TickerTransform.BeginAnimation(System.Windows.Media.TranslateTransform.XProperty, animation);
        }

        private void Minimize_Click(object sender, RoutedEventArgs e)
        {
            WindowState = WindowState.Minimized;
        }

        private void Maximize_Click(object sender, RoutedEventArgs e)
        {
            WindowState = WindowState == WindowState.Maximized ? WindowState.Normal : WindowState.Maximized;
        }

        private void Close_Click(object sender,RoutedEventArgs e)
        {
            Close();
        }

        private void TopBar_MouseLeftButtonDown(object sender, System.Windows.Input.MouseButtonEventArgs e)
        {
            if (e.ClickCount == 2)
            {
                WindowState = WindowState == WindowState.Maximized ? WindowState.Normal : WindowState.Maximized;
                return;
            }

            if (e.LeftButton ==
                System.Windows.Input.MouseButtonState.Pressed)
            {
                DragMove();
            }
        }
    }
}
