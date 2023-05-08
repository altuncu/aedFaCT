const IP_ADDRESS = "<ENTER SERVER IP ADDRESS HERE!>";
const PORT = "<ENTER SERVER PORT HERE!>";

chrome.runtime.onInstalled.addListener(function () {
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function () {
        chrome.declarativeContent.onPageChanged.addRules([{
            conditions: [new chrome.declarativeContent.PageStateMatcher({})],
            actions: [new chrome.declarativeContent.ShowPageAction()]
        }]);
    });
});

// Storage to save extracted keywords for each URL
var storage = chrome.storage.local;

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if ("getKeywords" == request.message) {
        chrome.tabs.query({
            "active": true,
            "currentWindow": true
        },
            function (tabs) {
                storage.get(tabs[0].url, function (result) {
                    if (tabs[0] && "undefined" != typeof tabs[0].id && tabs[0].id && result[tabs[0].url] != undefined) {
                        sendResponse({
                            "message": "keywords",
                            "keywords": result[tabs[0].url]
                        });
                    }
                    else if (tabs[0] && "undefined" != typeof tabs[0].id && tabs[0].id) {
                        var payload = {
                            url: tabs[0].url
                        };
                        fetch(`http://${IP_ADDRESS}:${PORT}/extract-keywords/`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(payload)
                        }).then(function (response) {
                            return response.json()
                        }).then(function (json) {
                            sendResponse({
                                "message": "keywords",
                                "keywords": JSON.parse(json["keywords"])
                            });
                            storage.set({
                                [tabs[0].url]: JSON.parse(json["keywords"])
                            }, function () {
                                console.log("Keywords saved in the local storage");
                            });
                        }).catch(function (ex) {
                            console.log('parsing failed', ex)
                        })
                    }
                });
            }
        );
    }

    else if ("searchInfo" == request.message) {
        chrome.tabs.query({
            "active": true,
            "currentWindow": true
        },
            function (tabs) {
                if (tabs[0] && "undefined" != typeof tabs[0].id && tabs[0].id) {
                    chrome.tabs.create({ url: 'results.html', active: true }, function (tab) {
                        console.log("Tab created");
                        var payload = {
                            keywords: request.selected
                        };

                        Promise.all([
                            fetch(`http://${IP_ADDRESS}:${PORT}/get-pubs/`, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify(payload)
                            }).then(function (response) {
                                console.log("Response: " + response);
                                return response.json()
                            }).then(function (json) {
                                chrome.tabs.sendMessage(tab.id, {
                                    action: "pubs-researchers",
                                    results: {
                                        "publications": JSON.parse(json["publications"]),
                                        "researchers": JSON.parse(json["researchers"])
                                    }
                                });
                            }).catch(function (ex) {
                                console.log('parsing failed for publications', ex)
                            }),
                            fetch(`http://${IP_ADDRESS}:${PORT}/get-news/`, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify(payload)
                            }).then(function (response) {
                                console.log("Response: " + response);
                                return response.json()
                            }).then(function (json) {
                                chrome.tabs.sendMessage(tab.id, {
                                    action: "news-articles",
                                    results: {
                                        "articles": JSON.parse(json["articles"])
                                    }
                                });
                            }).catch(function (ex) {
                                console.log('parsing failed for news articles', ex)
                            })]).then(function () {
                                console.log("All promises resolved");
                                chrome.tabs.sendMessage(tab.id, {
                                    action: "all-results-received"
                                });
                            });
                    });

                }
            }

        );
    }

    return true;
});
