# webdevparser
Web Deviation Parser
Deviations is a term used by quality control for when someone does something that does not comply with company SOPs or standards. This app is written to process deviations that are output by a specific vendors system.

The input file is a csv and contains the following fields:<br>

<table>
  <tr>
    <td>Center</td>
    <td>Location name or code</td>
  </tr>
  <tr>
    <td>ReferenceNumber</td>
    <td>Unique record identifier</td>
  </tr>
  <tr>
    <td>DateCreated</td>
    <td>Date the record was created</td>
  </tr>
  <tr>
    <td>DaysOpen</td>
    <td>number of days the issue has been opened</td>
  </tr>
  <tr>
    <td>Status</td>
    <td>Open, closed, etc</td>
  </tr>
  <tr>
    <td>DateClosed</td>
    <td>The date the issue was resolved</td>
  </tr>
  <tr>
    <td>ImpactCategory</td>
    <td>Minor, major, etc</td>
  </tr>
  <tr>
    <td>ErrorCode</td>
    <td>Error code or description</td>
  </tr>
  <tr>
    <td>RootCause</td>
    <td>What cause was attributed to the event</td>
  </tr>
  <tr>
    <td>EmployeesInvolved</td>
    <td>Employees listed on seperate lines</td>
  </tr>
  <tr>
    <td>Description</td>
    <td>Description of the event</td>
  </tr>
  <tr>
    <td>AssociatedDeviationCAPANumber</td>
    <td>Unique identifier for the deviation type</td>
  </tr>
</table>

The user uploads the csv file and the following processes are executed:<br>
<ol>
  <li>Get list of unique employee names is extracted.</li>
  <li>Create Excel file with a tab for each employee.</li>
  <li>For each employee, find each record containing their name and copy that record to their tab.</li>
  <li>Count the number of deviations per empolyee and output it to a summary file (csv).</li>
  <li>Output both files back to the user.</li>
</ol>
  
  This should be done without any files being written to disk to prevent others from accessing the files, for security purposes.  
