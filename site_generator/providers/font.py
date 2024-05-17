from site_generator.providers.provider import Provider
import base64

ROBOTO_400 = "roboto_400.woff2"
ROBOTO_700 = "roboto_700.woff2"
# From https://fonts.googleapis.com/css2?family=Roboto:wght@400;700, only using latin
ROBOTO_400_URL = (
    "https://fonts.gstatic.com/s/roboto/v30/KFOmCnqEu92Fr1Mu4mxKKTU1Kg.woff2"
)
ROBOTO_700_URL = (
    "https://fonts.gstatic.com/s/roboto/v30/KFOlCnqEu92Fr1MmWUlfBBc4AMP6lQ.woff2"
)


class Font(Provider):
    def get(self) -> list[str]:
        roboto_400 = self._get_encoded_font(ROBOTO_400, ROBOTO_400_URL)
        roboto_700 = self._get_encoded_font(ROBOTO_700, ROBOTO_700_URL)

        font_face_roboto_400 = self._get_font_face(weight=400, base64_font=roboto_400)
        font_face_roboto_700 = self._get_font_face(weight=700, base64_font=roboto_700)

        return [font_face_roboto_400, font_face_roboto_700]

    def _get_encoded_font(self, file_name: str, remote_file_url: str):
        file_content = self._download(file_name, remote_file_url)
        encoded = base64.b64encode(file_content)

        return encoded.decode("utf-8")

    def _get_font_face(self, **kwargs):
        font_face = """
            @font-face {{
                font-family: 'Roboto';
                font-style: normal;
                font-weight: {weight};
                src: url(data:font/woff2;base64,{base64_font}) format('woff2');
            }}
        """

        return font_face.format(**kwargs)
