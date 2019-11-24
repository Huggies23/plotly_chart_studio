# Basic plotly chart studio

## Introduction

This basic app allows the user to upload a csv with a column with common x-values, and a column for each trace containing the y-values.

An example of the csv structure is shown below (dataframe structure read using pandas.read_csv())

A [live instance of this app](https://huggies23-plotly-chart-studio.herokuapp.com/app) is hosted on Heroku. This has limited functionality and users will be unable to upload their own data or download any plot generated (other than a low res .png using the "export" button in the ploty toolbar).

## Features to add - 24 November 2019

1) restore default layout style
2) improve speed of .cslayout import and plot
3) more layout parameters in tabs (inc. x-axis etc.)
4) add trace options
5) improve data table view (and make editable?)