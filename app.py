from xml.sax import make_parser
from xml.sax.saxutils import prepare_input_source

from jinja2 import Environment, PackageLoader, select_autoescape

from alto.parser.alto import Alto
from alto.converter import prepare_alto

def main():
    parser = make_parser()
    alto = Alto(parser)

    with open("alto.xml", "r") as f:
        source = prepare_input_source(f)
        alto.parse(source)

    print("Parsed")

    hocr = prepare_alto(alto)

    print("Converted")

    env = Environment(loader=PackageLoader("alto.converter", "templates"),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template("hocr.html")
    print(template.render(language={"lang": "en"}, hocr=hocr))

if __name__ == "__main__":
    main()
