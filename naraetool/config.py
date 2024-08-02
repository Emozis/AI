import yaml
from typing import List
from pathlib import Path 
from naraetool.main_logger import logger 

class Config:
    def __init__(self, filenames:List[str]) -> None:
        self.filenames = filenames
        self.default_dir = Path(__file__).parents[1] / "config"
        self._set_attributes()
        

    def _read_yaml(self, filepath):
        with open(filepath, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)

        return config
    
    def _merge_data(self):
        configs = {}
        for filename in self.filenames:
            filepath = self.default_dir / f"{filename}_config.yaml"
            config = self._read_yaml(filepath)

            configs.update(config)    

        return configs
    
    def _set_attributes(self):
        merge_config = self._merge_data()
        for key, value in merge_config.items():
            setattr(self, key, value)

        logger.info(f"There are {len(merge_config)} configs {list(merge_config.keys())}")

config = Config(["persona", "project"])
