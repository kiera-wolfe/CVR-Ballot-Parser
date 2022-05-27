# CVR Ballot Reader

## Requirement

This product assumes that a working browser is installed.

This product uses Python. To install Python, follow the official guide for Python
[here](https://www.python.org/downloads/).

This product uses Bokeh and other libraries to display the graphical elements. To install Bokeh, one can use `pip` by
typing the following line in the terminal (command line).

```bash
pip install --user bokeh
```

Alternatively, one can follow the guidelines in the official guide for Bokeh
[here](https://docs.bokeh.org/en/latest/docs/user_guide/quickstart.html#userguide-quickstart-install).

To install Pandas use `pip` by typing the following line in the terminal (command line).

```bash
pip install pandas
```

## Running

### Using the Batch File

Step 1. Copy and paste or move the CVR file that you wish to read into the **_CVR Folder_**.
        Copy the name of the file you have moved as it will be needed in the next step.
        
Step 2. Open the **_config.yaml_** file in any basic text editor.
        Copy the CVR filename used in Step 1 in the _location_ section as in the example below.
        Be sure to include the quotations around the filename.
        
```bash        
location: "ExampleCVR.csv"
```

Step 3. Edit each line as necessary according to the CVR file used and the desired output.
        
Step 4. Run the **_View CVR Results_** batch file.
        Execute this batch file by double clicking.
        A press enter after verifying Step 1 and 2 are completed.
        
Step 5. When you are done viewing the CVR file you can exit the browser window and close the terminal.
        Repeat these steps for each CVR you wish to view.


### Running on Command Line

Follow Steps 1 and 2 above prior to using the command line.

To run the product, one can type the following line in the terminal.

```bash
bokeh serve --show display.py
```

This will create a (private) Bokeh server (listening to port 5006), and open a browser tab showing
the graph.

Subsequently, one can also type `http://localhost:5006` in the browser to see and interact with
the same graph.

When finished, one can press <kbd>Shift</kbd> + <kbd>C</kbd> to stop the server.

### Advanced

When multiple server sessions are required (e.g., when multiple auditors are reviewing different
part of the same dataset), each reviewer should decide a unique port number `PORT` between 1000
and 65535, and type the following line in the terminal.

```bash
bokeh serve --port PORT --show display.py
```

For example, if a reviewer uses `5007` as the port number, then they should type `bokeh serve
--port 5007 --show display`.

## Interactions

The plot shows the votes of a single ballot, when the "Ballot" selection is not set to "all", and
shows the summary of an entire batch of ballots otherwise.

One can click on the drop-down menus and select different choices to inspect different individual
ballots or to check the overview of a batch of ballots.

