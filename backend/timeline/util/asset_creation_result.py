
class AssetCreationResult:
    
    def __init__(self):
        self.versions_applied = []
        self.asset_id = ''
        self.path         = ''
        self.file_present = False
        self.exists_in_db = False
        self.version_in_db = False
        self.created_in_db = False
        self.version_saved = 0
