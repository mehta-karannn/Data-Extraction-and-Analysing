# Data-Extraction-and-Analysing

This repository contains a Python script to extract text from articles given in a list of URLs and perform textual analysis. The analysis computes several text-related variables and saves the results in a specified format.

## Objective

The objective of this is to:
1. Extract textual data from articles available at the given URLs.
2. Perform text analysis to compute various variables.
3. Save the results in an output file in a specified format.

## Data Extraction

For each URL provided in `Input.xlsx`, the script extracts the article title and text and saves it in a text file named with the URL_ID. The text extraction avoids including website headers, footers, or other non-article content.

## Data Analysis

The script performs text analysis on the extracted text and computes the following variables:
- POSITIVE SCORE
- NEGATIVE SCORE
- POLARITY SCORE
- SUBJECTIVITY SCORE
- AVG SENTENCE LENGTH
- PERCENTAGE OF COMPLEX WORDS
- FOG INDEX
- AVG NUMBER OF WORDS PER SENTENCE
- COMPLEX WORD COUNT
- WORD COUNT
- SYLLABLE PER WORD
- PERSONAL PRONOUNS
- AVG WORD LENGTH

The results are saved in an output file (`Output.xlsx`) following the format specified in `Output Data Structure.xlsx`.




