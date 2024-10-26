# Auto-Classifier

Auto-Classifier is a powerful tool that generates an automated classifier given an input dataset and a category column. This project aims to streamline the process of creating classification prompts based on user-provided data.

## Features

- Upload CSV or Excel datasets
- Select category and input text columns
- Provide additional context for categories
- Automatically detect unique categories
- Generate category descriptions using LLM
- Create interactive classification interface

## How It Works

1. **Data Upload**: Users upload a dataset (CSV or Excel) and select the category column, input text column(s), and provide context about the categories.

2. **Category Detection**: The system automatically detects unique categories present in the specified column.

3. **Description Generation**: For each category, an LLM is called with a user-defined maximum number of samples to generate a category description.

4. **Prompt Creation**: Category descriptions are collated into a new, improved classification prompt.

5. **Interactive Classification**: Users can input text for the chosen columns, and the system predicts the most likely category based on the generated prompt.

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/auto-classifier.git
   cd auto-classifier
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```
   streamlit run streamlit_app/app.py
   ```

4. Open your web browser and navigate to the provided local URL (usually http://localhost:8501).

## Usage

1. Upload your dataset using the file uploader in the app.
2. Select the predictor columns (input text) and the target column (categories).
3. Adjust the analysis settings in the sidebar, including samples per target and additional context.
4. Click "Analyze Columns" to start the classification process.
5. Review the results and use the interactive classification interface to test the model.

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- OpenAI API key (for GPT-4 access)
- Anthropic API key (for Claude access)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
