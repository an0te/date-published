# URL Publication & Modification Date Analyzer

This project is a Streamlit-based web application that allows users to input a list of URLs, extract publication and modification dates from JSON-LD embedded in HTML, and visualize the data. The tool is useful for analyzing the publication and update trends of articles across multiple URLs.

## Features

- **Input**: Paste a list of URLs into a text field.
- **Data Extraction**: Automatically parse the publication and modification dates from JSON-LD in the HTML of the given URLs.
- **Visualization**:
  - Number of articles published per year.
  - Number of articles modified per year.
  - Cumulative timeline showing the growth in the number of articles published over time.
- **CSV Download**: Export the parsed data as a CSV file for further analysis.
- **Sidebar**: Information about the tool and the technology stack used.

## How to Use

1. Clone the repository:

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run datepublished.py
   ```

4. Open your browser and navigate to the Streamlit local server (usually `http://localhost:8501`).
5. Paste the list of URLs into the text box, click the "Process URLs" button, and view the results in the table and visualizations.

## Example Output

After processing the URLs, the app will display the following:
* A table with the URLs, publication dates, and modification dates.
* Bar charts showing the number of articles published and modified per year.
* A cumulative timeline that visualizes the growth in the number of articles published.

## Technology Stack

* **Streamlit**: For the web interface and interactive visualizations.
* **Pandas**: For data manipulation and analysis.
* **Altair**: For creating the interactive charts and visualizations.
* **Requests**: For fetching HTML content from the provided URLs.

## Project Structure

```
url-date-analyzer/
│
├── datepublished.py           # Main Streamlit application
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue with suggestions and improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.