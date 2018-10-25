function updateBadge(tabId, text, color){
	browser.browserAction.setBadgeText({'text' : text.toString(), 'tabId' : tabId});
	browser.browserAction.setBadgeBackgroundColor({'color' : color, 'tabId' : tabId});
}
function validCertificates(tabId){
	updateBadge(tabId, '✓', 'green');
}
function invalidCertificates(tabId){
	updateBadge(tabId, '✗', 'red');
}


let getCurrentTab = browser => {
  return browser.tabs.getCurrent();
};
getCurrentTab(browser).then(validCertificates);

var log = console.log.bind(console);
var ALL_SITES = { urls: ['<all_urls>'], types: ['main_frame'] };
var extraInfoSpec = ['blocking'];

const serv_location = 'http://127.0.0.1:8080/?action=check&stream=stream1&hash=';

const certificates = Array();
const checked_fingerprints = Array();

browser.webRequest.onHeadersReceived.addListener(async function(details){
	var tabId = details.tabId;
	var requestId = details.requestId;
	var securityInfo = await browser.webRequest.getSecurityInfo(requestId, {
		certificateChain: true,
		rawDER: false
	});

	for(cert_rank in securityInfo.certificates){
		let certificate = securityInfo.certificates[cert_rank];
		let sha256_digest = certificate.fingerprint.sha256.replace(/:/g, '').toLowerCase();

		if (checked_fingerprints.indexOf(certificate.fingerprint.sha256) != -1){
			continue;
		}

		certificates.push(certificate);
		checked_fingerprints.push(certificate.fingerprint.sha256);


		let req = new XMLHttpRequest();
		let req_location = serv_location + sha256_digest;
		req.open('GET', req_location, true);
		req.onload = function (e) {
			if (req.readyState === 4 && req.status === 200) {
				if (req.responseText == "invalid") {
					invalidCertificates(tabId);
					valid = false;
				}
				else if (req.responseText == "valid"){
					valid = true;
				}
				cert_idx = certificates.indexOf(certificate);
				newcert = certificates[cert_idx];
				newcert.is_bcvalid = valid;
				certificates[cert_idx] = newcert;
			}
		};
		req.onerror = function (e) {
			console.error(req.statusText);
		};
		req.send();
	}
}, ALL_SITES, extraInfoSpec)

browser.runtime.onConnect.addListener(function(port){
    port.onMessage.addListener(function(msg) {
		port.postMessage(certificates);
    });
});
