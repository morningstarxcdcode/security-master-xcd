# reporting/issue_reporter.py
import os

class IssueReporter:
    """
    The IssueReporter is your friendly messenger, responsible for taking
    the raw findings from the scanner and transforming them into clear,
    actionable, and human-readable reports. Its goal is to make complex
    security information easy to understand for everyone, from junior
    engineers to project managers.

    It ensures that all file paths are relative to the project's root,
    making reports portable and easy to navigate within any development
    environment.
    """
    def __init__(self, project_root):
        """
        Initializes the IssueReporter.

        Args:
            project_root (str): The absolute path to the root directory of
                                the project being scanned. This is crucial
                                for converting absolute file paths into
                                relative ones, which are much more useful
                                in reports.
        """
        self.project_root = project_root

    def _get_relative_path(self, absolute_path):
        """
        A helper function to convert an absolute file path into a path
        relative to the project's root. This makes reports cleaner and
        more universally applicable.
        """
        try:
            return os.path.relpath(absolute_path, self.project_root)
        except ValueError:
            # This can happen if paths are on different drives or malformed.
            # In such cases, we fall back to showing the full path.
            return absolute_path

    def format_vulnerability_report(self, vulnerability):
        """
        Formats a single detected vulnerability into a concise, eye-catching
        report block, designed for quick understanding.

        Args:
            vulnerability (dict): A dictionary containing the details of
                                  a single vulnerability.

        Returns:
            str: A multi-line string representing the formatted vulnerability
                 report, complete with ASCII art borders for visual clarity.
        """
        # Extracting and preparing data for the report.
        # We use .get() with a default value to prevent errors if a key is missing.
        title = vulnerability.get("title", "Unknown Vulnerability")
        file_path_absolute = vulnerability.get("file", "N/A")
        file_path_relative = self._get_relative_path(file_path_absolute)
        line = vulnerability.get("line", "N/A")
        fix = vulnerability.get("fix", "No specific fix suggested.")
        severity = vulnerability.get("severity", "UNKNOWN").upper()
        status = vulnerability.get("status", "DETECTED").upper()
        autofix_status = vulnerability.get("autofix", "Not Available").replace("N/A", "Not Available")

        # Constructing the report with careful formatting for alignment.
        # The f-string formatting `:<width` ensures left alignment and padding.
        report = f"""
+----------------------------------------+
| [!] ALERT: {title:<22} |
+----------------------------------------+
| File: {file_path_relative:<29} |
| Line: {str(line):<29} |
| Fix: {fix:<32} |
| Severity: {severity:<25} |
| Status: {status:<27} |
| Autofix: {autofix_status:<26} |
+----------------------------------------+
"""
        return report

    def format_manual_fix_guidance(self, vulnerability):
        """
        Generates detailed guidance for vulnerabilities that require manual
        intervention. This section provides a clear summary, identifies
        affected components, outlines steps to fix, and provides a link
        to more information.

        Args:
            vulnerability (dict): A dictionary containing the details of
                                  a single vulnerability.

        Returns:
            str: A multi-line string providing human-readable guidance for
                 manual remediation.
        """
        # Extracting information, similar to the vulnerability report.
        title = vulnerability.get("title", "Unknown Issue")
        file_path_absolute = vulnerability.get("file", "N/A")
        file_path_relative = self._get_relative_path(file_path_absolute)
        line = vulnerability.get("line", "N/A")
        fix_steps = vulnerability.get("fix", "Consult documentation or security team.")
        advisory_url = vulnerability.get("advisory_url", "No specific URL provided.")

        # Constructing the guidance message.
        guidance = f"""
--- Manual Intervention Required ---
  Summary: {title}
  Affected Components: {file_path_relative} (Line: {line})
  Steps to Fix: {fix_steps}
  For more details, please consult the advisory: {advisory_url}
------------------------------------
"""
        return guidance