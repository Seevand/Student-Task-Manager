document.addEventListener('click', (event) => {

    const opener = event.target.closest('[data-dialog-target]');

    if (opener) {

        const dialog = document.querySelector(
            opener.dataset.dialogTarget
        );

        if (dialog && typeof dialog.showModal === 'function') {

            dialog.showModal();

        }

    }



    const closer = event.target.closest('[data-dialog-close]');

    if (closer) {

        closer.closest('dialog')?.close();

    }

});



document.querySelectorAll('dialog.dialog').forEach((dialog) => {

    dialog.addEventListener('click', (event) => {

        if (event.target === dialog) {

            dialog.close();

        }

    });

});
