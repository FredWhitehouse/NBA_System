# Example Python script concept (not fully implemented)
import os
import glob

def generate_project_summary(root_directory):
    summary = ["# Project Structure and Contents\n"]
    
    # Add directory structure
    summary.append("## Directory Structure\n```")
    # Code to get directory structure...
    summary.append("```\n")
    
    # Add file snippets for key files
    summary.append("## Key Files\n")
    # Code to get content of important files...
    
    # Write to summary file
    with open("project_summary.md", "w") as f:
        f.write("\n".join(summary))