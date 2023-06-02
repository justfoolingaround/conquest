from typing import Optional, Dict, List, TYPE_CHECKING


if TYPE_CHECKING:
    from . import TLSClients


class Settings:
    def __init__(
        self,
        client_identifier: Optional["TLSClients"] = None,
        ja3_string: Optional[str] = None,
        h2_settings: Optional[Dict[str, int]] = None,
        h2_settings_order: Optional[List[str]] = None,
        supported_signature_algorithms: Optional[List[str]] = None,
        supported_delegated_credentials_algorithms: Optional[List[str]] = None,
        supported_versions: Optional[List[str]] = None,
        key_share_curves: Optional[List[str]] = None,
        cert_compression_algo: Optional[str] = None,
        additional_decode: Optional[str] = None,
        pseudo_header_order: Optional[List[str]] = None,
        connection_flow: Optional[int] = None,
        priority_frames: Optional[List[str]] = None,
        header_order: Optional[List[str]] = None,
        header_priority: Optional[Dict] = None,
        random_tls_extension_order: bool = False,
        force_http1: bool = False,
        catch_panics: bool = False,
        debug: bool = False,
    ):
        self.client_identifier = client_identifier
        self.ja3_string = ja3_string

        self.h2_settings = h2_settings
        self.h2_settings_order = h2_settings_order

        self.supported_signature_algorithms = supported_signature_algorithms
        self.supported_delegated_credentials_algorithms = (
            supported_delegated_credentials_algorithms
        )

        self.supported_versions = supported_versions
        self.key_share_curves = key_share_curves

        self.cert_compression_algo = cert_compression_algo
        self.additional_decode = additional_decode
        self.pseudo_header_order = pseudo_header_order
        self.connection_flow = connection_flow
        self.priority_frames = priority_frames
        self.header_order = header_order
        self.header_priority = header_priority
        self.random_tls_extension_order = random_tls_extension_order
        self.force_http1 = force_http1
        self.catch_panics = catch_panics
        self.debug = debug

    def get(self) -> Dict:
        request_payload = {
            "forceHttp1": self.force_http1,
            "withDebug": self.debug,
            "catchPanics": self.catch_panics,
            "headerOrder": self.header_order,
            "additionalDecode": self.additional_decode,
        }

        if self.client_identifier is None:
            custom_tls_client = {}

            if self.ja3_string is not None:
                custom_tls_client["ja3String"] = self.ja3_string

            if self.h2_settings is not None:
                custom_tls_client["h2Settings"] = self.h2_settings

            if self.h2_settings_order is not None:
                custom_tls_client["h2SettingsOrder"] = self.h2_settings_order

            if self.pseudo_header_order is not None:
                custom_tls_client["pseudoHeaderOrder"] = self.pseudo_header_order

            if self.connection_flow is not None:
                custom_tls_client["connectionFlow"] = self.connection_flow

            if self.priority_frames is not None:
                custom_tls_client["priorityFrames"] = self.priority_frames

            if self.header_priority is not None:
                custom_tls_client["headerPriority"] = self.header_priority

            if self.cert_compression_algo is not None:
                custom_tls_client["certCompressionAlgo"] = self.cert_compression_algo

            if self.supported_versions is not None:
                custom_tls_client["supportedVersions"] = self.supported_versions

            if self.supported_signature_algorithms is not None:
                custom_tls_client[
                    "supportedSignatureAlgorithms"
                ] = self.supported_signature_algorithms

            if self.supported_delegated_credentials_algorithms is not None:
                custom_tls_client[
                    "supportedDelegatedCredentialsAlgorithms"
                ] = self.supported_delegated_credentials_algorithms

            if self.key_share_curves is not None:
                custom_tls_client["keyShareCurves"] = self.key_share_curves

            if custom_tls_client:
                request_payload["customTlsClient"] = custom_tls_client

        else:
            request_payload["tlsClientIdentifier"] = self.client_identifier.value
            request_payload[
                "withRandomTLSExtensionOrder"
            ] = self.random_tls_extension_order

        return request_payload
