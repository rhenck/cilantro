import logging
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

server = "ojs"
port = "80"
auth_key = "YWRtaW4=:cGFzc3dvcmQ="

log = logging.getLogger(__name__)


def generate_frontmatter(article_id):
    """
    Generate frontmatter page for articles in OJS via Frontmatter-Plugin.

    Does a simple GET request to the OJS plugin passing on IDs of documents
    already present in OJSself.

    Authorization is done with a specific test user.

    :param article_id: ID of the article in OJS
    :return: tuple containing the response code and text
    """
    headers = {'ojsAuthorization': auth_key}

    url = (f"http://{server}:{port}"
           f"/ojs/plugins/generic/ojs-cilantro-plugin/api/frontmatters/"
           f"create/article/?id={article_id}")

    return _make_request(url, headers)


def publish(import_xml_file_path, journalcode):
    """
    Publish the documents referenced in the passed XML via OJS-Import-Plugin.

    The paramter file contains OJS-specific XML which contains file paths to
    documents which shall be imported to OJS. It is read and passed to a POST
    request (in UTF-8) to the OJS import plugin.

    Server address and port can be given optionally.

    The Import-Plugin needs authentication which is (for now) hard-coded.

    :param str import_xml_file_path: OJS-Import-XML
    :param str journalcode: Name of the journal that will be imported to
    :return: Tuple of return code and text of the POST request to OJS
    """
    with open(import_xml_file_path, "r") as f:
        import_data = f.read()

    headers = {'Content-Type': 'application/xml',
               'ojsAuthorization': auth_key}

    request_url = (f"http://{server}:{port}"
                   f"/ojs/plugins/generic/ojs-cilantro-plugin/api/import/"
                   f"{journalcode}")

    return _make_request(request_url, headers,
                         import_data.encode(encoding='utf-8'))


def _make_request(url, headers, import_data=None):
    """Make the request to OJS and return response code and content."""
    log.debug(f"Request: URL: {url} Headers: {headers} Data: {import_data}")

    request = Request(url, headers=headers,
                      data=import_data)

    try:
        with urlopen(request) as response:
            response_text = response.read().decode('utf-8')
    except HTTPError as e:
        log.debug(f"Request failed with: {e.read()}")
        raise

    return response.getcode(), json.loads(response_text)
