import pandas as pd
import os


def load_data():
    """Load the bidding data from CSV file."""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data\\boss_merge.csv')
    df = pd.read_csv(data_path)
    
    # Clean column names by stripping whitespace
    df.columns = df.columns.str.strip()
    
    # Clean string columns by stripping whitespace
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
    
    # Convert numeric columns
    df['Median Bid'] = pd.to_numeric(df['Median Bid'], errors='coerce')
    df['Min Bid'] = pd.to_numeric(df['Min Bid'], errors='coerce')
    
    return df


def get_course_options(df):
    """Get course options for dropdown with truncated descriptions."""
    courses = df[['Course Code', 'Description']].drop_duplicates()
    options = []
    
    for _, row in courses.iterrows():
        course_code = row['Course Code']
        description = row['Description']
        
        # Create the full label text
        full_label = f"{course_code} -> {description}"
        
        # Truncate if longer than 40 characters
        if len(full_label) > 50:
            truncated_label = full_label[:50] + "..."
        else:
            truncated_label = full_label
        
        options.append({
            'label': truncated_label,
            'value': course_code,
            'title': full_label  # Full text shown on hover
        })
    
    return sorted(options, key=lambda x: x['value'])


def get_bidding_window_options(df):
    """Get bidding window options for dropdown."""
    windows = df['Bidding Window'].unique()
    return [{'label': window, 'value': window} for window in sorted(windows)]


def get_instructor_options(df, course_code=None, bidding_window=None):
    """Get instructor options for dropdown, optionally filtered by course and window."""
    filtered_df = df.copy()
    
    if course_code:
        filtered_df = filtered_df[filtered_df['Course Code'] == course_code]
    
    if bidding_window:
        filtered_df = filtered_df[filtered_df['Bidding Window'] == bidding_window]
    
    instructors = filtered_df['Instructor'].unique()
    return [{'label': instructor, 'value': instructor} for instructor in sorted(instructors)]


def get_section_options(df, course_code=None, bidding_window=None, instructor=None):
    """Get section options for checkboxes, filtered by selections."""
    filtered_df = df.copy()
    
    if course_code:
        filtered_df = filtered_df[filtered_df['Course Code'] == course_code]
    
    if bidding_window:
        filtered_df = filtered_df[filtered_df['Bidding Window'] == bidding_window]
    
    if instructor:
        filtered_df = filtered_df[filtered_df['Instructor'] == instructor]
    
    sections = filtered_df['Section'].unique()
    return [{'label': section, 'value': section} for section in sorted(sections)]


def get_school_department_options(df):
    """Get school/department options for dropdown."""
    schools = df['School/Department'].unique()
    return [{'label': school, 'value': school} for school in sorted(schools)]


def get_all_terms():
    """Get all possible terms from 2021-22 Term 2 to 2024-25 Term 2."""
    all_terms = []
    
    # Generate all terms from 2021-22 to 2024-25
    for start_year in range(2021, 2026):
        end_year = start_year + 1
        year_str = f"{start_year}-{str(end_year)[2:]}"
        
        for term in range(1, 3):
            all_terms.append(f"{year_str} Term {term}")
    
    return all_terms


def sort_terms(terms):
    """Sort terms chronologically."""
    def term_sort_key(term):
        # Parse term like "2021-22 Term 2"
        try:
            year_part, term_part = term.split(' Term ')
            start_year = int(year_part.split('-')[0])
            term_num = int(term_part)
            return (start_year, term_num)
        except:
            return (0, 0)
    
    return sorted(terms, key=term_sort_key)


def filter_data(df, school_department=None, course_code=None, bidding_window=None, instructor=None, sections=None):
    """Filter data based on user selections."""
    filtered_df = df.copy()
    
    if school_department:
        filtered_df = filtered_df[filtered_df['School/Department'] == school_department]
    
    if course_code:
        filtered_df = filtered_df[filtered_df['Course Code'] == course_code]
    
    if bidding_window:
        filtered_df = filtered_df[filtered_df['Bidding Window'] == bidding_window]
    
    if instructor:
        filtered_df = filtered_df[filtered_df['Instructor'] == instructor]
    
    if sections:
        filtered_df = filtered_df[filtered_df['Section'].isin(sections)]
    
    return filtered_df
