pragma solidity >= 0.8.11 <= 0.8.11;

contract CertificateVerification {
    string public company_details;
    string public certificate_details;

    function setCompanyDetails(string memory cd) public {
        company_details = cd;	
    }

    function getCompanyDetails() public view returns (string memory) {
        return company_details;
    }

    function setCertificateDetails(string memory cd) public {
        certificate_details = cd;	
    }

    function getCertificateDetails() public view returns (string memory) {
        return certificate_details;
    }

    constructor() public {
        company_details = "empty";
	certificate_details = "empty";
    }
}