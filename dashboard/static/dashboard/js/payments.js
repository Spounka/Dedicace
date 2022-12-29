let urlString = "";
let url = null;

window.onload = function () {
    windowLoad();
};


function windowLoad() {
    urlString = window.location.href;
    url = new URL(urlString)
    let searchbar = document.getElementById('searchbar-input');
    searchbar.addEventListener('keydown', function (e) {
        if (searchbar.value === "") {
            return
        }
        if (e.code === "Enter") {
            setSearchQuery('search', searchbar.value);
        }
    });

    let cards = document.getElementsByClassName('payment-object');
    for (const card of cards) {
        card.addEventListener('click', e => {
            $('#from').html(card.dataset.sender);
            $('#to').html(card.dataset.recepient);
            $('#amount').html(card.dataset.amount + " Dzd");
            let input = document.getElementById('file-path-input');
            input.value = card.dataset.img
            $('.ui.modal').modal('show');
        })
    }

    let downloadImg = document.getElementById('download-img')
    downloadImg.addEventListener('click', e => {
        $('#download-file-form').submit();
    });
}

function setSearchQuery(key, value) {
    if (url.searchParams.get(key)) {
        url.searchParams.set(key, value)
    } else {
        url.searchParams.append(key, value)
    }
    console.log(url.toString())
    window.location.assign(url)
}

function clearQueries() {
    if (urlString.includes("?")) urlString = urlString.split('?')[0];
    url = new URL(urlString)
    window.location.href = url.toString()
}

