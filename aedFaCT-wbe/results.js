const numArticles = 5, numPubs = 5, numExperts = 5; // Number of results to show per page
var pagesArticles, pagesPubs, pagesExperts;
var totalArticles, totalPubs, totalExperts;
var percentage = 0;
let currentArticles = 1, currentPubs = 1, currentExperts = 1;

chrome.runtime.onMessage.addListener(
    function(request) {
        if (request.action == "pubs-researchers") {
            percentage += 50;
            document.getElementById("text").textContent = "Searching for scientific publications...";
            document.getElementById("progressBar").style.width = String(percentage) + "%";
            totalPubs = request.results.publications;
            totalExperts = request.results.researchers;
        }
        else if (request.action == "news-articles") {
            percentage += 50;
            document.getElementById("text").textContent = "Searching for news articles...";
            document.getElementById("progressBar").style.width = String(percentage) + "%";
            totalArticles = request.results.articles;
        }
        else if (request.action == "all-results-received") {
            try {
                document.getElementById("progressBarContainer").style.display = "none";
                document.getElementById("results").style.display = "block";
                
                pagesArticles = Math.ceil(totalArticles.length / numArticles);
                console.log("Number of articles found: ", totalArticles.length);
                var infoArticles = document.createElement('p');
                infoArticles.innerHTML = `<b>${totalArticles.length} articles found</b>`;
                news_tab = document.getElementById("news");
                news_tab.appendChild(infoArticles);
                newArticles(totalArticles);
                for (var i = 0; i < Math.min(totalArticles.length, numArticles); i++) {
                    news_tab.getElementsByClassName("itemBox")[i].style.display = "block";
                }
                if (totalArticles.length > numArticles) {
                    var loadMore = document.createElement('button');
                    loadMore.setAttribute("id", "loadMoreNews");
                    loadMore.className = "loadMore";
                    loadMore.innerHTML = "Load more";
                    document.getElementById("news").appendChild(loadMore);
                    loadMore.onclick = function() {
                        currentArticles++;
                        newPage = Array.from(news_tab.getElementsByClassName("itemBox")).slice((currentArticles-1)*numArticles, currentArticles*numArticles);
                        for (var i = 0; i < newPage.length; i++) {
                            newPage[i].style.display = "block";
                        }
                        if (currentArticles == pagesArticles) {
                            this.style.display = "none";
                        }
                    }
                }
            } catch (error) {
                var infoArticles = document.createElement('p');
                infoArticles.innerHTML = `<b>Error showing the result: ${error}</b>`;
                news_tab = document.getElementById("news");
                news_tab.appendChild(infoArticles);
            }
            
            try {
                pagesPubs = Math.ceil(totalPubs.length / numPubs);
                console.log("Number of publications found: ", totalPubs.length);
                var infoPubs = document.createElement('p');
                infoPubs.innerHTML = `<b>${totalPubs.length} publications found</b>`;
                papers_tab = document.getElementById("papers");
                papers_tab.appendChild(infoPubs);
                newPubs(totalPubs);
                for (var i = 0; i < Math.min(totalPubs.length, numPubs); i++) {
                    papers_tab.getElementsByClassName("itemBox")[i].style.display = "block";
                }
                if (totalPubs.length > numPubs) {
                    var loadMore = document.createElement('button');
                    loadMore.setAttribute("id", "loadMorePubs");
                    loadMore.className = "loadMore";
                    loadMore.innerHTML = "Load more";
                    document.getElementById("papers").appendChild(loadMore);
                    loadMore.onclick = function() {
                        currentPubs++;
                        newPage = Array.from(papers_tab.getElementsByClassName("itemBox")).slice((currentPubs-1)*numPubs, currentPubs*numPubs);
                        for (var i = 0; i < newPage.length; i++) {
                            newPage[i].style.display = "block";
                        }
                        if (currentPubs == pagesPubs) {
                            this.style.display = "none";
                        }
                    }
                }
            } catch (error) {
                var infoPubs = document.createElement('p');
                infoPubs.innerHTML = `<b>Error showing the result: ${error}</b>`;
                papers_tab = document.getElementById("papers");
                papers_tab.appendChild(infoPubs);
            }
            
            try {
                pagesExperts = Math.ceil(totalExperts.length / numExperts);
                console.log("Number of researchers found: ", totalExperts.length);
                var infoExperts = document.createElement('p');
                infoExperts.innerHTML = `<b>${totalExperts.length} researchers found</b>`;
                researchers_tab = document.getElementById("researchers");
                researchers_tab.appendChild(infoExperts);
                newExperts(totalExperts);
                for (var i = 0; i < Math.min(totalExperts.length, numExperts); i++) {
                    researchers_tab.getElementsByClassName("itemBox")[i].style.display = "block";
                }
                if (totalExperts.length > numExperts) {
                    var loadMore = document.createElement('button');
                    loadMore.setAttribute("id", "loadMoreExperts");
                    loadMore.className = "loadMore";
                    loadMore.innerHTML = "Load more";
                    document.getElementById("researchers").appendChild(loadMore);
                    loadMore.onclick = function() {
                        currentExperts++;
                        newPage = Array.from(researchers_tab.getElementsByClassName("itemBox")).slice((currentExperts-1)*numExperts, currentExperts*numExperts);
                        for (var i = 0; i < newPage.length; i++) {
                            newPage[i].style.display = "block";
                        }
                        if (currentExperts == pagesExperts) {
                            this.style.display = "none";
                        }
                    }
                }
            } catch (error) {
                var infoExperts = document.createElement('p');
                infoExperts.innerHTML = `<b>Error showing the result: ${error}</b>`;
                researchers_tab = document.getElementById("researchers");
                researchers_tab.appendChild(infoExperts);
            }
            
        }        
});

// Function to create the news panels
function newArticles(array) {
    array.forEach(a => {
        var news_panel = document.createElement('button');
        if (a.source_category == "mainstream") {
            icon = "fa fa-newspaper-o";
            verification_status = "verified";
            cred_rating_url = `<a href="${a.cred_rating_url}" target="_blank"><i class="fa fa-check"></i></a>`;
            source = ``;
        } else if (a.source_category == "science") {
            icon = "fa fa-flask";
            verification_status = "verified";
            cred_rating_url = `<a href="${a.cred_rating_url}" target="_blank"><i class="fa fa-check"></i></a>`;
        } else {
            icon = "fa fa-globe";
            verification_status = "unverified";
            cred_rating_url = ``;
        }
        news_panel.className = "itemBox";
        news_panel.innerHTML = `<a style="text-decoration: none;" href=" ${a.url} " target="_blank">
                                    <i class="${icon} w3-xlarge xw3-margin-right"></i>
                                    <b>${a.title} (<mark class="${verification_status}">${a.source}</a> ${cred_rating_url} 
                                <a style="text-decoration: none;" href=" ${a.url} " target="_blank"></mark> - ${a.date})</b>
                                <p style="font-family: Arial, Helvetica, sans-serif; font-size: 14px;">${a.comments}</p></a>`
        console.log(news_panel.innerHTML);
        news_tab = document.getElementById("news");
        news_tab.appendChild(news_panel);
    });
}

// Function to create the publication panels
function newPubs(array) {
    array.forEach(p => {
        var coll_button = document.createElement('button');
        coll_button.className = "itemBox";
        coll_button.innerHTML = `<a style="text-decoration: none;" href=" ${p.doi_link} " target="_blank"><i class="fa fa-book w3-xlarge xw3-margin-right"></i> <b>${p.title} (${p.venue}, ${p.year})</b>
                                 <p style="font-family: Arial, Helvetica, sans-serif; font-size: 14px;"><b>Abstract: </b>${p.highlighted_abstract}</p><p style="font-family: Arial, Helvetica, sans-serif; font-size: 13px;"><i><b>Authors: </b>${p.authors_str}</i></p></a>`;
        papers_tab = document.getElementById("papers");
        papers_tab.appendChild(coll_button);
    });
}

// Function to create the expert panels
function newExperts(array) {
    array.forEach(e => {
        var exp_button = document.createElement('button');
        exp_button.className = "itemBox";
        var other_links = "";
        var related_pubs = "";
        if (e.other_links != null) {
            e.other_links.forEach(l => {
                other_links = `<a href="${l}" target="_blank"><p style="text-indent: 20px; text-decoration: none;"><i class="fa fa-link w3-xlarge xw3-margin-right"></i> ${l}</p></a>`;
            });
        }
        if (e.related_pubs != null) {
            e.related_pubs.forEach(p => {
                related_pubs += `<p style="text-indent: 20px;"><i class="fa fa-book w3-xlarge xw3-margin-right"></i> ${p}</p>`;
            });
        }
        exp_button.innerHTML = `<a style="text-decoration: none;" href=" ${e.scopus_link} " target="_blank"><i class="fa fa-user solid w3-xlarge xw3-margin-right"></i>
                                <b>${e.full_name} (${e.affiliation})</b></a>` + other_links + related_pubs;
        researchers_tab = document.getElementById("researchers");
        researchers_tab.appendChild(exp_button);
    });
}

function openTab(evt, tabName) {
    var i, x, tablinks;
    x = document.getElementsByClassName("city");
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

document.getElementById("newsTab").addEventListener("click", function() {
    openTab(event, "news");
});

document.getElementById("papersTab").addEventListener("click", function() {
    openTab(event, "papers");
});

document.getElementById("researchersTab").addEventListener("click", function() {
    openTab(event, "researchers");
});


