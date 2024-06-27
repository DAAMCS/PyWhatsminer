from core.api import WhatsminerAPI, WhatsminerAccessToken
from core.models import Summary, Status, Api, Dev, Devs, DevDetail, DevDetails, Pool, Pools
from core.utils import process_response

from typing import Any

from deprecated import deprecated


class System:
    """
    This class provides methods for miner's system.
    """
    def __init__(self, client):
        self.client = client
        self.api: WhatsminerAPI = client.api
        self.token: WhatsminerAccessToken = client._access_token
        
    
    def reboot(self) -> Any:
        """
        This operation simply reboots miner's system.
        """
        return self.api.exec_command(self.token, "reboot")


    def reset(self) -> Any:
        """
        This operation resets the miner to factory settings.
        """
        return self.api.exec_command(self.token, "factory_reset")
    
    
    # TODO: Check status model
    def get_status(self) -> Status:
        """
        This method returns miner's status.
        
        WARNING: Response model can be incorrect. Will be fixed in the future.
        """
        data = process_response(self.api.exec_command(self.token, "status"))

        return Status(*data['Msg'].values())
    
    
    def get_summary(self) -> Summary:
        """
        This method returns miner's summary.
        """
        data = process_response(self.api.exec_command(self.token, "summary"))
        summary = process_response(data['SUMMARY'][0])
        
        return Summary(*summary.values())
    
    
    def get_api_version(self) -> Api:
        """
        This method returns miner's API version.
        """
        data = process_response(self.api.exec_command(self.token, "get_version"))
    
        return Api(*data['Msg'].values())
    
    
    def get_dev_details(self) -> DevDetails:
        """
        This method returns miner's device details.
        """
        data = self.api.exec_command(self.token, "devdetails")
        devdetails = DevDetails(details=[])
        
        for devdetail in data['DEVDETAILS']:
            devdetail = process_response(devdetail)
            devdetail.pop('ID')
            devdetails.details.append(DevDetail(*devdetail.values()))
    
        return devdetails
    
    
    def get_devs(self) -> Devs:
        """
        This method returns information for each hash board.
        """
        data = self.api.exec_command(self.token, "devs")
        devs = Devs(devs=[])
    
        for dev in data['DEVS']:
            dev = process_response(dev)
            devs.devs.append(Dev(*dev.values()))
    
        return devs
    
    
    def get_pools(self) -> Pools:
        """
        This method returns pool miner information.
        """
        data = self.api.exec_command(self.token, "pools")
        pools = Pools(pools=[])
        
        for pool in data['POOLS']:
            pool = process_response(pool)
            pools.pools.append(Pool(*pool.values()))
            
        return pools    
    
    
    # TODO: Implement this
    @deprecated(reason="Not work. Will be implemented in the future.")
    def get_token(self) -> Any:
        """
        This method returns miner's access token.
        
        WARNING: This method actually not work. Will be implemented in the future.
        """
        return self.api.exec_command(self.token, "get_token")
    