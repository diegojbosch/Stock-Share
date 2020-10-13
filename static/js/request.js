function setFrame() {
	var keywords = document.getElementById("keywords").value;
	var queryParams = '?stock_ticker=' + keywords;
	
	var xhrCompanyOutlook = new XMLHttpRequest();
	xhrCompanyOutlook.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200) {
			var jsonResponse = JSON.parse(xhrCompanyOutlook.responseText);
			document.getElementById("companyOutlook").innerHTML = jsonResponse.description;

		}
	}
	
	xhrCompanyOutlook.open("GET", "http://localhost:5000/api/v1.0/company-outlook" + queryParams, false);
    xhrCompanyOutlook.send();
	
	var xhrStockSummary = new XMLHttpRequest();
	xhrStockSummary.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200) {
			var jsonResponse = JSON.parse(xhrStockSummary.responseText);
			document.getElementById("stockSummary").innerHTML = jsonResponse.highPrice;
		}
	}
	
	xhrStockSummary.open("GET", "http://localhost:5000/api/v1.0/stock-information" + queryParams, false);
	xhrStockSummary.send();
	
	var xhrNewsArticles = new XMLHttpRequest();
	xhrNewsArticles.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200) {
			var jsonResponse = JSON.parse(xhrNewsArticles.responseText);
			document.getElementById("latestNews").innerHTML = jsonResponse[0].data;
		}
	}
	
	xhrNewsArticles.open("GET", "http://localhost:5000/api/v1.0/news-articles" + queryParams, false);
	xhrNewsArticles.send();
	
	document.getElementById("results").classList.remove("hide");
	document.getElementById("results").classList.add("showResults");
	//show first tab
	document.getElementById("companyOutlook").style.display = "block";
}

function clearResults(){
    document.getElementById("results").innerHTML = "";
    return false;
}

function changeTab(event, info) {
	var tabContent, tablinks;
	tabContent = document.getElementsByClassName("tabContent");
	
	for (var i=0; i<tabContent.length; i++) {
		tabContent[i].style.display = "none";
	}
	
	tabLinks = document.getElementsByClassName("tabLinks");
	
	for (var i=0; i<tabLinks.length; i++) {
		tabLinks[i].className = tabLinks[i].className.replace(" active", "");
	}
	
	document.getElementById(info).style.display = "block";
	event.currentTarget.className += " active";
}