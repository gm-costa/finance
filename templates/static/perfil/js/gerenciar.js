function mostrar_barra_vertical(url) {
    
    //const divContas = document.getElementById('div-contas');
    const divContas = document.querySelector('.div-contas');
    const listaContas = document.querySelectorAll('.lista-conta');
    const divCategorias = document.querySelector('.div-categorias');
    
    const qtd_linhas = 5;
    let alturaContas = 0;

    fetch(url, {
        method: 'GET',
    }).then(function (result) {
        return result.json();
    }).then(function (data) {
        if(data.qtd_contas > qtd_linhas) {
            divContas.classList.add('barra-vertical');
            for(let i = 0; i < listaContas.length; i++) {
                listaContas[i].classList.add('me-2');
                if(i < qtd_linhas) {
                    alturaContas += parseInt(listaContas[i].getBoundingClientRect().height) + 16;
                };
            };
        } else {
            divContas.classList.remove('barra-vertical');
            for(let i = 0; i < listaContas.length; i++) {
                listaContas[i].classList.remove('me-2');
                alturaContas += parseInt(listaContas[i].getBoundingClientRect().height) + 16;
            };
        };
        divContas.style.height = alturaContas.toString() + 'px';

        if(divCategorias !== null) {
            let alturaCategorias = 0;
            const listaCategorias = document.querySelectorAll('.lista-categoria');

            if(data.qtd_categorias > 3) {
                divCategorias.classList.add('barra-vertical');
                for(let i = 0; i < listaCategorias.length; i++) {
                    listaCategorias[i].classList.add('me-2');
                    if(i < 3) {
                        alturaCategorias += parseInt(listaCategorias[i].getBoundingClientRect().height) + 16;
                    };
                };
            } else {
                divCategorias.classList.remove('barra-vertical');
                for(let i = 0; i < listaCategorias.length; i++) {
                    listaCategorias[i].classList.remove('me-2');
                    alturaCategorias += parseInt(listaCategorias[i].getBoundingClientRect().height) + 16;
                };
            };
            divCategorias.style.height = alturaCategorias.toString() + 'px';
        };
    })
}
