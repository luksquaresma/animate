import json, sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import utils

class Element():
    # this is a polymorphic class intended to represent 
    # all the possible elements inside a diagram
    def __init__(self, element_type, element_properties):

        self.type = element_type        
        
        # loading of standard config file
        if "element_config" not in globals():
            with open("./elements.json", "r") as file:
                globals()["element_config"] = dict(json.load(file))
        _config = globals()["element_config"]

        # element dimention definition
        def find_element_dimensions(element_type):
            _keys = [k for (k, v) in _config["dimension"].items() if element_type in v]
            if len(_keys) == 1:
                return _keys[0]
            else:
                sys.exit("Panic: Stopping the program!") 
        self.dimension = find_element_dimensions(element_type)

        # property difeinition
        if all(
            #checks if all properties are present
            k in _config["dimension_properties"][self.dimension]
            for k in element_properties.keys()
        ):
            for key in _config["dimension_properties"][self.dimension]:
                try:
                    setattr(self, key, element_properties[key])
                except Exception as E:
                    print("Error on element definition:")
                    print(E)
                    raise
        else:
            raise ValueError("Missing element properties!")

    # returns the plotly objet to the
    def plot_on(self, fig, ax):
        match self.dimension:
            case "0D":
                ret = plt.scatter(x=self.position[0], y=self.position[1], color="k")
            case "1D":
                match self.type:
                    case "line":
                        ret = plt.plot(
                            [self.start[0], self.end[0]],
                            [self.start[1], self.end[1]],
                            color="k",
                            )
                    case "arrow":
                        ret = plt.arrow(
                            x=self.start[0],
                            y=self.start[1], 
                            dx=(self.end[0] - self.start[0]),
                            dy=(self.end[1] - self.start[1]),
                            color="k",
                            length_includes_head=True,
                            head_width=0.03,
                            capstyle="round"
                            )
            #     ret = plt.
            # case "2D":
        
        if type(ret) == type(list()):
            utils.unpack_nested_lists(ret)

        if hasattr(ret, 'get_path'):
            mpl.collections.PathCollection(ret.get_path())
            

        return ret