### Prompt 1
I want to build a python dash application based on the following dataset in sample_data.csv

The dashboard should show this:

### User search
1. A search bar with a dropdown menu, where users can either
- Click the dropdown and it will show options like CS102 -> Programming Fundamentals, CS205 -> Operating systems, basically mapping "Course Code" -> "Description" 
- Type in the Course Code like CS102 and as users search, the drop down selection will be filtered to follow their query

2. A dropdown menu of the "Bidding Window", which will show which window they want to filter the chart by, whether it be "Round 1 Window 1" or "Round 1A Window 1".

3. Another dropdown menu of the "Instructor" which will further filter down the chart

4. Another list that will show checkboxes of the "Sections" column. If multiple checkboxes are selected, there will be multiple charts that will be displayed in a grid of 3 cols.

### Dashboard results
1. In each col grid, there is a multi line chart view that will show the data for the selected Course Code, Bidding Window, Instructor and section. If there are multiple sections, it will show multiplle charts in the grid.
- The x axis would be the "Term" column, which is sorted by the earliest term to latest term
- The y axis would be the "Median Bid" and "Min Bid" column, which will show the numerical
- It will display the change in price of the course across the change in term.

### Considerations
- I am using uv python package manager for installing libraries
- let me know if there's anything unclear

### Best practices for dash app structure
my_dash_app/
├── app.py             # instantiate Dash() and import server if deploying to Flask/Werkzeug
├── index.py           # entry‐point: imports app.layout & callbacks, then app.run_server()
├── requirements.txt   # list of PyPI deps (dash, pandas, etc.)
│
├── assets/            # special folder auto‐served by Dash
│   ├── style.css      # global CSS
│   └── logo.png       # any other static files (JS, fonts, images)
│
├── data/              # raw or processed data files
│   └── sample_data.csv
│
├── layouts/           # layouts broken into pages or sections
│   ├── __init__.py
│   └── main_layout.py
│
├── callbacks/         # callbacks grouped by feature
│   ├── __init__.py
│   └── filtering.py
│
├── components/        # reusable UI pieces
│   ├── __init__.py
│   ├── navbar.py
│   └── footer.py
│
└── utils/             # helper functions, data loaders, constants
    ├── __init__.py
    └── data_loader.py


### Prompt 2

It still doesn't work. Maybe to be more specific in my issues, for the Dropdown menus, when the text in the dropdown is greater than the width of the dropdown component, the text will wrap. However, the clickable part of the dropdown does not expand with the words. Is there any way for this to be fixed? If not, I'm ok witha  workaround as well, maybe by putting the search course and bidding window in the top part? so the structure will be like such
<div class="row">
    <SearchCourse/>
    <BiddingWindow/>
</div>
<div class="row">
    <!-- The side bar -->
    <div class="col"> 
        <Instructor/>
        <Sections/>
    </div>
    <div class="col">
        <ChartDisplay/>
    </div>
</div>

### Prompt 3
Things I would like to change:
1. I want to add in an additional filter dropdown button in the dashboard that comes as the first filter step to allow people to filter by the School/Department column in the csv file. 
2. I also want each displayed chart's x axis to always show the minimum term, which is 2021-22 Term 2, to the max term, which is 2024-25 Term 2, in the chart, even when there is missing data.

Can you help me implement the changes in my python dash app?


### Prompt 4
can you change the main layout so that the School/Department, Search Course, Bidding Window, and Instructor are all in 1 column stacked on each other at the top? Then additional filters can have sections alone? The layout would look like:
<div>
    <col>
        <School/>
        <Search/>
        <Bidding/>
        <Instructor/>
    </col>
    <row>
        <col>
            <Sections/>
        </col>
        <col>
            <ChartDisplay/>
        </col>
    </row>
</div>