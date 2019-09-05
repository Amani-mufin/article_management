function openClose(detailsId) {
    const more = document.getElementById(detailsId);
    console.log(detailsId);
    if (more.style.display === 'block') {
      more.style.display = 'none';
    } else {
      more.style.display = 'block';
    }
  }