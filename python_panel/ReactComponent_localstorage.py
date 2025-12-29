import panel as pn
import datetime
import json
    

from panel.custom import ReactComponent


class PythonJSRoundtripExample(ReactComponent):

    _esm = """
    function send_event(model, key_list = []) {
      // get local storage items and send back to python
      let storageItemsObj = {};
      for (const key of key_list) {
        storageItemsObj[key] = localStorage.getItem(key);
      }
      model.send_msg(JSON.stringify(storageItemsObj));
    }

    function parseJsonToLocalStorage(jsonString) {
      console.log("Parsing JSON and storing to localStorage:", jsonString);
      try {
        const data = JSON.parse(jsonString);
        for (const key in data.store_obj) {
          if (data.store_obj.hasOwnProperty(key)) {
            localStorage.setItem(key, data.store_obj[key]);
            console.log(`Stored ${key}: ${data.store_obj[key]} in localStorage`);
          }
        }
      } catch (e) {
        console.error("Invalid JSON string:", e);
      }
    }

    export function render({ model }) {
      const [value, setValue] = React.useState(null)

      model.on('msg:custom', (msg) => {
        console.log("Received message from Python:", msg)
        parseJsonToLocalStorage(msg);

        // get key_list from python message if any
        let key_list = [];
        try {
          const data = JSON.parse(msg);
          if (data.get_list) {
            key_list = data.get_list;
          }
        } catch (e) {
          console.error("Invalid JSON string:", e);
        }
        send_event(model, key_list)
      })

      return <div></div>
    }
    """

    def send_event(self, save_str):
        if save_str == "":
            print("retrieving stored string")
            self._send_msg(json.dumps({"get_list":["save_str"]}))
        else:
            print("storing string: ", save_str)
            self._send_msg(json.dumps({"store_obj":{"save_str": save_str},
                                   "get_list":["save_str"]}))

    def _handle_msg(self, msg):
        msg = json.loads(msg).get("save_str", None)
        
        print("\n stored string is: ", msg, "\n\n")



if __name__ == "__main__":
    import time
    py2js = PythonJSRoundtripExample()

    pn.serve(py2js, port = 8888, threaded=True)

    while True:
        command = input("type \n(a) non-empty string to store string \n(b) empty string to retrieve stored string\n" \
        "")

        py2js.send_event(command)  
        time.sleep(1)  # wait for message to be processed