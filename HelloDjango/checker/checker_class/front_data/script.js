$(document).ready(function(){
    $.fn.removeClassStartingWith = function (filter) {
        $(this).removeClass(function (index, className) {
            return (className.match(new RegExp("\\S*" + filter + "\\S*", 'g')) || []).join(' ')
                });
            return this;
            };

        const queryString = window.location.search;
        isDebug = false;
        let errorCount = 0;
        let debugClass = '__debug';
        let debugMsgClass = '__debug_msg';
        let formNoSelectClass = '__debug_no_select';
        let fromInputNotelClass = '__debug_no_tel';
        let debugScritpDate = '__debug_script_date'
        function onOffDebug(){
            if (isDebug){
                updateErrorMarker();
                findAlla();
                FormSelectBebug();
                formInputType();
                findPrice();
                findCurrency();
                findImgLink();
                findSpanWarning();
                findSriptsDate();
            }
            else{
                removeAllDebug()
            }

        }
        function getMsg(){
            let msg = $('<span></span>')
            msg.addClass(debugMsgClass)
            console.log(msg, 'getMsg')
            return msg
        }
        function removeAllDebug(){
            let forms = $('form.'+formNoSelectClass)
            forms.removeClass(formNoSelectClass)
            let scriptDate = $('.' + debugScritpDate).removeClass(debugScritpDate)
            $('input').removeClass(fromInputNotelClass)
            x = document.querySelectorAll('.__debug');
            for (pos in x){
                let elem = x[pos]
                if (elem.classList != undefined){
                    elem.classList.remove(debugClass);
                }
            }
            removeDebugMsg()


        }
        function removeDebugMsg(){
            let msgs = $('.' + debugMsgClass)
            console.log(msgs.length, 'msgs')
            msgs.remove()
        }

        function FormSelectBebug(){
            let forms = $('form')
            let formsNoSelect = forms.filter(function(){
                if($(this).find('select').length == 0){
                    return true
                }
            })

            formsNoSelect.addClass(formNoSelectClass)
            console.log(formsNoSelect.length, 'xxxxx')
            formsNoSelect.each(function(){
                let msg = getMsg()
                msg.text('No select')
                $(this).append(msg)
                plusError()
            })

        }

        function formInputType(){
            let inputs = $('form input[name=phone]')
            console.log(inputs)
            let inputsNoTel = inputs.filter(function(){
                if ($(this).attr('type') != 'tel'){
                    return true
                }
            })
            console.log(inputsNoTel)
            inputsNoTel.addClass(fromInputNotelClass)
            if (inputsNoTel.length != 0){plusError();}
        }


        function findAlla(){
            // поиск ссылок
            let links = $('a')
            links.addClass(debugClass)
        }
        function findPrice(){
            let oldPrice = $('.price_land_s4')
            let newPrice = $('.price_land_s1')
            oldPrice.addClass(debugClass)
            newPrice.addClass(debugClass)

        }
        function findCurrency(){
            let currencys = $('.price_land_curr')
            currencys.addClass(debugClass)
        }

        function findImgLink(){
            let imgs = $('a img')
            imgs.addClass(debugClass)

        }
        function findSpanWarning(){
            let elems = $('span.back-warning')
            elems.addClass(debugClass)
        }
        function plusError(){
            errorCount ++
            updateErrorMarker()
        }
        function updateErrorMarker(){
            let marker = $('#oi-toolbar .error-counter .marker')
            let markerInfo = $('#oi-toolbar .error-counter .info')
            if (errorCount == 0){
                marker.css('background-color', 'green')

            } else {
                marker.css('background-color', 'red')
            }
            markerInfo.text(errorCount)
        }
        $('#oi-toolbar .io-main').click(function(){
            $('#oi-toolbar #back-info').toggle(300)
        })

        $('#oi-toolbar .original-link p').click(function(){
            let url = $(this).attr('data-href')
            console.log(url)
            window.open(url, '_blank').focus();
        })

        // Поиск элементов с script внутри (возможно это скрипт даты)
        function findSriptsDate(){
//            let elems = $('body script').parent()
        let elems = $('body script')
            elems = elems.filter(function(){
                if ($(this).is('body') != true) {return true}
            })
            elems.addClass(debugScritpDate)
            elems.text('!!!')
        }

        let oiToolbar = $('#oi-toolbar')
        $(document).keyup(function(e) {
            if (e.ctrlKey && e.keyCode == 73) {
                console.log('INTEGRATIONS')
                if (isDebug){isDebug = false}else{isDebug = true}
                oiToolbar.toggle(500)
                onOffDebug()
            }
    });
})