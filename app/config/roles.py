class Roles:
    '''
    Constant Roles
    
    :var CIVIC: Description
    :vartype CIVIC: Literal['civic']
    :var FACILITY: Description
    :vartype FACILITY: Literal['facility']
    :var COLLECTOR: Description
    :vartype COLLECTOR: Literal['collector']
    :var DISPOSAL: Description
    :vartype DISPOSAL: Literal['disposal']
    :var CITIZEN: Description
    :vartype CITIZEN: Literal['citizen']
    :var ALL: Description
    :vartype ALL: list[str]
    '''

    CIVIC = "civic"
    FACILITY = "facility"
    COLLECTOR = "collector"
    DISPOSAL = "disposal"
    CITIZEN = "citizen"

    ALL = [
        CIVIC,
        FACILITY,
        COLLECTOR,
        DISPOSAL,
        CITIZEN
    ]
