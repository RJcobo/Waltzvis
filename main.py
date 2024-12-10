from audio_analysis import AudioAnalyzer
from mygraphic import PygletVisualizer

def main():
    # Initialize components
    audio_analyzer = AudioAnalyzer()
    visualizer = PygletVisualizer()

    # Start audio stream
    audio_analyzer.start_stream()

    # Update function to fetch audio data
    def update_callback():
        return audio_analyzer.get_frequency_spectrum()

    # Run the visualizer
    try:
        visualizer.run(update_callback)
    except KeyboardInterrupt:
        print("Exiting")
    finally:
        audio_analyzer.stop_stream()

if __name__ == "__main__":
    main()
