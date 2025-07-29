function loadCategories(typeId) {
    const categorySelect = document.getElementById('id_category');
    const subcategorySelect = document.getElementById('id_subcategory');

    if (!typeId) {
        categorySelect.innerHTML = '<option value="">Выберите Тип</option>';
        subcategorySelect.innerHTML = '<option value="">Выберите категорию</option>';
        return;
    }

    fetch(`/api/get-categories/${typeId}/`)
        .then(response => response.json())
        .then(data => {
            categorySelect.innerHTML = '<option value="">Выберите категорию</option>';
            data.forEach(item => {
                const option = new Option(item.name, item.id);
                categorySelect.appendChild(option);
            });

            subcategorySelect.innerHTML = '<option value="">Выберите подкатегорию</option>';
        })
        .catch(error => console.error('Ошибка загрузки категорий:', error));
}


function loadSubcategories(categoryId) {
    const subcategorySelect = document.getElementById('id_subcategory');

    if (!categoryId) {
        subcategorySelect.innerHTML = '<option value="">Выберите категорию</option>';
        return;
    }

    fetch(`/api/get-subcategories/${categoryId}/`)
        .then(response => response.json())
        .then(data => {
            subcategorySelect.innerHTML = '<option value="">Выберите подкатегорию</option>';
            data.forEach(item => {
                const option = new Option(item.name, item.id);
                subcategorySelect.appendChild(option);
            });
        })
        .catch(error => console.error('Ошибка загрузки подкатегорий:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    const typeSelect = document.getElementById('id_type');
    const categorySelect = document.getElementById('id_category');

    if (typeSelect) {
        typeSelect.addEventListener('change', function() {
            loadCategories(this.value);
        });

        if (typeSelect.value) {
            loadCategories(typeSelect.value);
        }
    }

    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            loadSubcategories(this.value);
        });

        if (categorySelect.value) {
            loadSubcategories(categorySelect.value);
        }
    }
});