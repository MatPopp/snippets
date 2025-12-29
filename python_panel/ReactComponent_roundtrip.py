import panel as pn
import datetime

from panel.custom import ReactComponent


class PythonJSRoundtripExample(ReactComponent):

    _esm = """
    function send_event(model) {
      model.send_msg("hello back from javascript")
    }

    export function render({ model }) {
      const [value, setValue] = React.useState(null)

      model.on('msg:custom', (msg) => {
        console.log("Received message from Python:", msg)
        send_event(model)
      })

      return <div></div>
    }
    """

    def send_event(self):
        self._send_msg("hello to javascript at " + str(datetime.datetime.now()))

    def _handle_msg(self, msg):
        print(msg)


if __name__ == "__main__":
    py2js = PythonJSRoundtripExample()

    pn.serve(py2js, threaded=True)

    while True:
        input("Press Enter to send current time to JS...")
        py2js.send_event()  