# [Return Period Calculator](https://github.com/COMP0016-IFRC-Team5/data-visualiser) 

A data visualizer tool produces the return period-loss graph of low-impact hazardous events for 91 countries. This tool use publicly available data from national disaster loss databases (DesInventar) and EM-DAT, but also available for other resources.  

This tool is a part of a UCL IXN project, Define return periods for low-impact hazardous events with IFRC. 

 

 ### Project Introduction 

Define return periods for low-impact hazardous events  

IFRC and individual Red Cross/Red Crescent National Societies are increasingly focusing on dedicating resources to take anticipatory action to mitigate the impacts of relatively high-frequency, low-intensity natural hazards. In other words, instead of reserving funds for those events that are expected to take place once every five years, IFRC and the National Societies aim to address events that occur more frequently, such as once per two or three years.  

In order to assess when an event (whether forecasted or already occurred) has reached the new threshold, we need to have impact exceedance curves based on observational data for these specific types of hazardous events. Using publicly available data from national disaster loss databases (DesInventar), EM-DAT, IFRC and other sources, the goal of this project would be to create exceedance curves and tables for multiple impacts for as many National Societies as possible. 

 

## Get Started 

**Check out our [online demo](https://github.com/COMP0016-IFRC-Team5/data-visualiser).** 

To build Period CalculatorPython locally, first, clone the source code:

```bash
git clone https://github.com/COMP0016-IFRC-Team5/data-visualiser
```

Then, let's install all package dependencies by running:

```bash
pip install -r requirements.txt
```

## Usage

To run the example, simply:

```bash
python example.py
```
To see available countries, call [visualiser.get_available_countries()](https://github.com/COMP0016-IFRC-Team5/data-visualiser/blob/main/example.py#L5) after setting the path of csv data file. The tool loaded with default 91 countries' data from DesInventar and EM-DAT.

```bash
print(visualiser.get_available_countries())
```

This tool supports stimultaneous access to graphs of different disasters in single or multiple countries, by switch between setting contents in variable [countries](https://github.com/COMP0016-IFRC-Team5/data-visualiser/blob/main/example.py#L6) and [country](https://github.com/COMP0016-IFRC-Team5/data-visualiser/blob/main/example.py#L7). 

To access graphs of multi-countries:

```bash
countries = ["<country name>", "<country name>", ..]
```


To access graphs of single country:

```bash
country = "<country name>"
```

Similar for events:

```bash
    events = ["<hazardous event name>",
              "<hazardous event name>", ..]
```

or

```bash
    event = "<hazardous event name>"
```


To choose sliced or orignial data, switch between [Folders.unsliced](https://github.com/COMP0016-IFRC-Team5/data-visualiser/blob/main/visualiser/_config.py#L7) and [Folders.sliced](https://github.com/COMP0016-IFRC-Team5/data-visualiser/blob/main/visualiser/_config.py#L7).

To choose sliced data:

```bash
__SELECTED_FOLDER = Folders.sliced
```

To choose unsliced data:

```bash
__SELECTED_FOLDER = Folders.unsliced
```

To deploy the tool for other data resource, call [visualiser.set_data_folder()](https://github.com/COMP0016-IFRC-Team5/data-visualiser/blob/main/example.py#L4) to set the path of target csv file. The data should be organized in format of [Country Name]/[Hazardous Events.csv]

 The data should contians these colomns:
 
| deaths         | directly_affected       | indirectly_affected	| start_date	 | secondary_end	 |
|----------------|-------------------------|---------------------|-------------|----------------|
| 0              | 100                     | 200               	 | 1911-02-18  | 1911-02-21     |
| 5              | 60                      | 300               	 | 1912-02-18  | 1912-02-21     |
| 3              | 100                     | 100               	 | 1914-02-18  | 1914-02-21     |
| 10             | 220                     | 400               	 | 1916-02-18  | 1916-02-21     |
