# Profile data editor
Profile data will be under something like `\AppData\Roaming\songsofsyx\saves\profile\`. The files are serialized in a custom(?) format.

* Convert from custom to JSON: `cat SavedPrints.txt | python to_json.py > prints.json`
* Convert JSON back to custom: `cat prints.json | python from_json.py > SavedPrints.txt`

Once you have the data in JSON, you can use your own tools to manipulate it however you want (see `example/`).
