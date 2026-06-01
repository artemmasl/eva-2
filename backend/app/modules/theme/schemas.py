from pydantic import BaseModel


class ThemeConfigSchema(BaseModel):
    primaryColor: str
    logo: str
    typography: str
    cardStyle: str
