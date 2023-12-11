# pylint: disable = C0114, C0115, C0116, R0903
from google.oauth2.service_account import Credentials
import pandas_gbq as pdg
import pandas as pd
from config import conf


class BQExporter:

    def __init__(self) -> None:
        self._cred = Credentials.from_service_account_file(
            conf.CRED_FILE
        )


    def export(self, df1, exists: str = 'append'):
        pdg.to_gbq(df1 , conf.BQ_TABLE,
        project_id=conf.BQ_PROJECT, if_exists=exists,
        credentials=self._cred)


    def query(self, query: str) -> pd.DataFrame:
        dataframe = pdg.read_gbq(
            query, project_id=conf.BQ_PROJECT,
            progress_bar_type=None,
            credentials=self._cred
            )
        return dataframe