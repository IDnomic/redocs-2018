 var body = document.getElementById("body");
 var port = browser.runtime.connect();
 port.postMessage();
 port.onMessage.addListener(function(msg) {
 	for (cert_idx in msg){
		cert = msg[cert_idx];
		var node = document.getElementsByClassName("cert")[0];
		var newnode = node.cloneNode(true);
		newnode.querySelector('.cert_fingerprint').innerHTML = cert.subject;
		if (cert.is_bcvalid){
			newnode.classList.add("valid");
		}
		else if (! cert.is_bcvalid){
			newnode.classList.add("invalid");
		}
		else {
			newnode.classList.add("normal");
		}
		newnode.style.display = "initial";
		body.appendChild(newnode);
	}
 });
