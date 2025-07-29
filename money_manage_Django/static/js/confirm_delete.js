document.querySelector('form').addEventListener('submit', function(e) {
    if (!confirm('Вы точно хотите удалить эту запись? Действие нельзя будет отменить.')) {
        e.preventDefault();
    }
});