function setFrame() {
	var keywords = document.getElementById("keywords").value;
	var queryParams = '?stock_ticker=' + keywords;
	var showResults = true;
	var htmlCode = '';
	var jsonResponse;
	
	var xhrCompanyOutlook = new XMLHttpRequest();
	xhrCompanyOutlook.open("GET", "http://localhost:5000/api/v1.0/company-outlook" + queryParams, false);
    xhrCompanyOutlook.send();
	
	if (xhrCompanyOutlook.readyState == 4 && xhrCompanyOutlook.status == 200) {
		
		jsonResponse = JSON.parse(xhrCompanyOutlook.responseText);
		
		htmlCode = '<table><tr><td style="width: 170px;"><b>Company name</b></td><td>' + jsonResponse.companyName + '</td></tr><tr><td><b>Stock Ticker Symbol</b></td><td>' + jsonResponse.stockTickerSymbol + '</td></tr><tr><td><b>Stock Exchange Code</b></td><td>' + jsonResponse.stockExchangeCode + '</td></tr><tr><td><b>Company Start Date</b></td><td>' + jsonResponse.companyStartDate + '</td></tr><tr><td><b>Description</b></td><td>' + jsonResponse.description + '</td></tr></table>';
		
		document.getElementById("companyOutlook").innerHTML = htmlCode;
		
	} else {
		showResults = false;
	}
	
	if(showResults){
		var xhrStockSummary = new XMLHttpRequest();
		xhrStockSummary.open("GET", "http://localhost:5000/api/v1.0/stock-information" + queryParams, false);
		xhrStockSummary.send();

		if(xhrStockSummary.readyState == 4 && xhrStockSummary.status == 200) {
			jsonResponse = JSON.parse(xhrStockSummary.responseText);
			htmlCode = '<table><tr><td><b>Stock Ticker Symbol</b></td><td>' + jsonResponse.stockTickerSymbol + '</td></tr><tr><td><b>Trading Day</b></td><td>' + jsonResponse.tradingDay + '</td></tr><tr><td><b>Previous Closing Price</b></td><td>' + jsonResponse.previousClosingPrice + '</td></tr><tr><td><b>Opening Price</b></td><td>' + jsonResponse.openingPrice + '</td></tr><tr><td><b>High Price</b></td><td>' + jsonResponse.highPrice + '</td></tr><tr><td><b>Low Price</b></td><td>' + jsonResponse.lowPrice + '</td></tr><tr><td><b>Last Price</b></td><td>' + jsonResponse.lastPrice + '</td></tr><tr><td><b>Change</b></td><td>' + jsonResponse.change + '</td></tr><tr><td><b>Change Percent</b></td><td>' + jsonResponse.changePercent + '</td></tr><tr><td><b>Number of Shares Traded</b></td><td>' + jsonResponse.numberSharesTraded + '</td></tr></table>';
			document.getElementById("stockSummary").innerHTML = htmlCode;
		} else {
			showResults = false;
		}
	}
	
	if(showResults){
		var xhrNewsArticles = new XMLHttpRequest();
		xhrNewsArticles.open("GET", "http://localhost:5000/api/v1.0/news-articles" + queryParams, false);
		xhrNewsArticles.send();

		if(xhrNewsArticles.readyState == 4 && xhrNewsArticles.status == 200) {
			jsonResponse = JSON.parse(xhrNewsArticles.responseText);
			htmlCode = '';
			for(var i=0; i<jsonResponse.length; i++){
				htmlCode += '<div class="show-card"><div class="image"><img src="' + jsonResponse[i].image + '"></div><div><p><b>' + jsonResponse[i].title + '</b></p><p>Published Date: ' + jsonResponse[i].data + '</p><p><a href="' + jsonResponse[i].linkOriginalPost + '">See original post</a></p></div></div>';
			}
			document.getElementById("latestNews").innerHTML = htmlCode;
		} else {
			showResults = false;
		}
	}
	
	if(showResults){
		document.getElementById("results").classList.remove("hide");
		document.getElementById("results").classList.add("showResults");
		//show first tab and make tab button active
		document.getElementById("companyOutlook").style.display = "block";
		document.getElementById("companyButton").className = "tabLinks active";
	} else {
		document.getElementById("noRecordFound").classList.remove("hide");
		document.getElementById("noRecordFound").classList.add("showError");
		document.getElementById("results").classList.remove("showResults");
		document.getElementById("results").classList.add("hide");
	}
}

function clearResults(){
    document.getElementById("results").innerHTML = "";
    return false;
}

function changeTab(button, info) {
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