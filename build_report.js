const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow,
  TableCell, WidthType, ShadingType, AlignmentType, LevelFormat,
} = require("docx");

const H = (text, level) => new Paragraph({ text, heading: level, spacing: { before: 240, after: 120 } });
const P = (text, opts = {}) => new Paragraph({ children: [new TextRun(text)], spacing: { after: 160 }, ...opts });
const Bullet = (text) => new Paragraph({
  text, numbering: { reference: "bullets", level: 0 }, spacing: { after: 80 },
});

function cell(text, opts = {}) {
  return new TableCell({
    width: { size: opts.width || 2000, type: WidthType.DXA },
    shading: opts.header ? { fill: "2F5496", type: ShadingType.CLEAR } : undefined,
    children: [new Paragraph({
      children: [new TextRun({ text, bold: !!opts.header, color: opts.header ? "FFFFFF" : undefined })],
    })],
  });
}

const colWidths = [2600, 3200, 3200];
const toolTable = new Table({
  columnWidths: colWidths,
  width: { size: 9000, type: WidthType.DXA },
  rows: [
    new TableRow({ children: [cell("Tool", { header: true, width: colWidths[0] }), cell("Purpose", { header: true, width: colWidths[1] }), cell("Used For", { header: true, width: colWidths[2] })] }),
    new TableRow({ children: [cell("NumPy", { width: colWidths[0] }), cell("Numerical computing", { width: colWidths[1] }), cell("Log transform, array operations", { width: colWidths[2] })] }),
    new TableRow({ children: [cell("Pandas", { width: colWidths[0] }), cell("Tabular data handling", { width: colWidths[1] }), cell("Loading, cleaning, grouping, merging", { width: colWidths[2] })] }),
    new TableRow({ children: [cell("Matplotlib", { width: colWidths[0] }), cell("Plotting", { width: colWidths[1] }), cell("Bar & line charts", { width: colWidths[2] })] }),
    new TableRow({ children: [cell("Seaborn", { width: colWidths[0] }), cell("Statistical visualization", { width: colWidths[1] }), cell("Histogram, scatter, box plot, heatmap", { width: colWidths[2] })] }),
    new TableRow({ children: [cell("Scikit-learn", { width: colWidths[0] }), cell("Preprocessing", { width: colWidths[1] }), cell("Min-max scaling of revenue", { width: colWidths[2] })] }),
  ],
});

const issueColWidths = [3000, 3000, 3000];
const issueTable = new Table({
  columnWidths: issueColWidths,
  width: { size: 9000, type: WidthType.DXA },
  rows: [
    new TableRow({ children: [cell("Issue Found", { header: true, width: issueColWidths[0] }), cell("Example", { header: true, width: issueColWidths[1] }), cell("Fix Applied", { header: true, width: issueColWidths[2] })] }),
    new TableRow({ children: [cell("Missing values", { width: issueColWidths[0] }), cell("price, quantity, customer_city, rating", { width: issueColWidths[1] }), cell("Median/mode imputation; rating left as NaN with a has_rating flag", { width: issueColWidths[2] })] }),
    new TableRow({ children: [cell("Duplicate rows", { width: issueColWidths[0] }), cell("4 duplicated order records", { width: issueColWidths[1] }), cell("Dropped with drop_duplicates()", { width: issueColWidths[2] })] }),
    new TableRow({ children: [cell("Inconsistent text casing", { width: issueColWidths[0] }), cell("\u201cdelhi\u201d vs \u201cDelhi\u201d", { width: issueColWidths[1] }), cell("Trimmed and title-cased", { width: issueColWidths[2] })] }),
    new TableRow({ children: [cell("Mixed date formats", { width: issueColWidths[0] }), cell("2026-01-22 vs 22/01/2026", { width: issueColWidths[1] }), cell("Parsed with pd.to_datetime(format='mixed')", { width: issueColWidths[2] })] }),
    new TableRow({ children: [cell("Wrong data type", { width: issueColWidths[0] }), cell("price stored as text: \u201cRs.799.0\u201d", { width: issueColWidths[1] }), cell("Currency prefix stripped, cast to float", { width: issueColWidths[2] })] }),
  ],
});

const doc = new Document({
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT }],
    }],
  },
  sections: [{
    properties: {
      page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } },
    },
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 80 },
        children: [new TextRun({ text: "Hands-On Data Lab Implementation", bold: true, size: 32 })],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 300 },
        children: [new TextRun({ text: "Task 2 Submission Report — Data Science Internship Program", italics: true, size: 22, color: "555555" })],
      }),

      H("1. Overview", HeadingLevel.HEADING_1),
      P("This report accompanies Hands_On_Data_Lab_Implementation.ipynb, submitted for Task 2 of the Data Science internship program. The notebook sets up a complete Data Science environment and applies it end-to-end to a simulated retail sales dataset, covering data loading, cleaning, Pandas/NumPy manipulation, visualization, and basic statistical analysis."),

      H("2. Environment Setup", HeadingLevel.HEADING_1),
      P("The following tools were installed and verified inside the notebook:"),
      toolTable,
      new Paragraph({ text: "", spacing: { after: 200 } }),

      H("3. Dataset", HeadingLevel.HEADING_1),
      P("A simulated retail sales log of 64 orders (data/retail_sales_raw.csv) was used, deliberately generated with realistic data-quality problems so the cleaning workflow could be demonstrated meaningfully rather than on already-clean data. A second lookup table (data/city_region_lookup.csv) mapping cities to regions was used to demonstrate merging."),

      H("4. Data Cleaning", HeadingLevel.HEADING_1),
      P("The following issues were identified and resolved before analysis:"),
      issueTable,
      new Paragraph({ text: "", spacing: { after: 200 } }),

      H("5. Pandas & NumPy Operations", HeadingLevel.HEADING_1),
      Bullet("Selection and multi-condition filtering (e.g. high-value rated orders)"),
      Bullet("Sorting orders by revenue"),
      Bullet("Grouping and aggregation of revenue, average price, and order count by category"),
      Bullet("Merging the sales data with the city-to-region lookup table"),
      Bullet("Derived columns: revenue, order_month, min-max scaled revenue, log-transformed revenue"),

      H("6. Visualizations Produced", HeadingLevel.HEADING_1),
      Bullet("Bar chart — total revenue by category"),
      Bullet("Line chart — monthly revenue trend"),
      Bullet("Histogram — distribution of order revenue"),
      Bullet("Scatter plot — price vs. quantity, colored by category"),
      Bullet("Box plot — revenue distribution by region"),
      Bullet("Heatmap — correlation matrix of price, quantity, revenue, and rating"),

      H("7. Key Observations", HeadingLevel.HEADING_1),
      Bullet("Fitness and Electronics categories generate the highest total revenue, driven by higher per-unit prices rather than order volume."),
      Bullet("Order revenue is right-skewed, with a small number of high-value orders raising the mean above the median."),
      Bullet("Price and revenue are strongly positively correlated, as expected since revenue = price \u00d7 quantity."),
      Bullet("Rating shows negligible correlation with price or quantity — customer satisfaction is not simply a function of spend."),
      Bullet("Cleaning (currency stripping, date unification, text standardization, imputation, de-duplication) was a necessary prerequisite for every downstream grouping, merge, and chart."),

      H("8. Conclusion", HeadingLevel.HEADING_1),
      P("This lab demonstrates a full, reproducible Data Science workflow: environment setup, ingestion of imperfect data, systematic cleaning, Pandas/NumPy-based manipulation, a five-chart visualization suite, and a short correlation-based analysis with clearly stated observations. All code, the cleaned dataset, and exported charts are included in the GitHub repository."),

      H("9. Repository", HeadingLevel.HEADING_1),
      P("GitHub repository: <insert your repository URL here after pushing>"),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  require("fs").writeFileSync("report.docx", buf);
  console.log("report.docx written");
});
