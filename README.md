# Basic plotly chart studio

## Introduction

This basic app allows the user to upload a csv with a column with common x-values, and a column for each trace containing the y-values.

An example of the csv structure is shown below (dataframe structure read using pandas.read_csv())

A [live instance of this app](https://huggies23-plotly-chart-studio.herokuapp.com/app) is hosted on Heroku. This has limited functionality and users will be unable to upload their own data or download any plot generated (other than a low res .png using the "export" button in the ploty toolbar).

## Features to add

1) restore default latout style
2) more layout parameters in tabs (inc. x-axis etc.)
3) add trace options
4) improve data table view (and make editable?)