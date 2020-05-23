"""This file serves as a hub for the Weight & Balance algorithms. import this file to a view for
    access to these algorithms"""
import json
from .DerivativeGrenerator import Derivative_Grenerator

# from .LimitsFinder import fuel_in_envelope_bisection


class CentrogramUtilites:
    @staticmethod
    def list_discrete_configs(client_request):
        """Converts client choices to discrete configurations

        Arguments:
            client_request {dict} -- deserialized JSON object holding the user's choices

        Returns:
            discrete_configs [list] -- list of dicts
        """
        try:
            server_data = json.loads(client_request)
            discrete_configs = Derivative_Grenerator(server_data)
        except json.JSONDecodeError as error:
            print("Error deserialize client request", error)
            return {}
        except TypeError as error:
            print("Error deserialize client request", error)
            return {}
        else:
            return discrete_configs

    @staticmethod
    def add_config_to_fuelflow(fuelflow, config_data):
        try:
            fuelflow_weight = fuelflow["weight"]
            fuelflow_moment_long = fuelflow["moment_long"]
            config_moment_long = config_data["Weight"] * config_data["CG"]
        except KeyError:
            print("KeyError: check if 'weight','moment_long','CG' keys exist ")
        config_moment_long = config_data["Weight"] * config_data["CG"]
        centrogram = {"name": config_data["items"], "weight": [], "cg_long": []}
        config_moment_long = config_data["Weight"] * config_data["CG"]

        for weight, moment in list(zip(fuelflow_weight, fuelflow_moment_long)):
            centrogram["weight"].append(weight + config_data["Weight"])
            centrogram["cg_long"].append(
                ((moment + config_moment_long) / (weight + config_data["Weight"]))
            )
        return centrogram

    @staticmethod
    def create_centrograms_from_configs(config, fuelflow):
        centrograms = []
        for tn_item in config:
            for derivative in tn_item["Derivatives"]:
                centrograms.append(
                    CentrogramUtilites.add_config_to_fuelflow(fuelflow, derivative)
                )
        return centrograms


class LimitiationsDeriving:
    @staticmethod
    def filter_centrograms(centrograms, envelope):
        pass

    @staticmethod
    def get_limits_from_centrogram(centrogram, envelope):
        pass

    @staticmethod
    def get_most_strict_limits(limits):
        pass


def get_limits(client_request):
    discrete_configs = CentrogramUtilites.list_discrete_configs(client_request)
    centrograms = CentrogramUtilites.create_centrograms_from_configs(
        discrete_configs, fuelflow
    )


if __name__ == "__main__":
    """Testing script - delete in prod
    """
    import json

    with open(
        "C:\\Tamnun\\TAMNUN_DEV\\TamnunProject\\TamnunMainPage\\DummyData\\DerivativeGeneratorTest1.json"
    ) as f:
        configs = json.loads(f.read())
    with open(
        "C:\\Tamnun\\TAMNUN_DEV\\TamnunProject\\TamnunMainPage\\DummyData\\fuelflow1.json"
    ) as f:
        fuelflow = json.loads(f.read())

    centrograms = CentrogramUtilites.create_cenrogram_from_configs(configs, fuelflow)

    with open(
        "C:\\Tamnun\\TAMNUN_DEV\\TamnunProject\\TamnunMainPage\\DummyData\\centrograms1.json",
        "w",
    ) as f:
        f.write(json.dumps(centrograms))
