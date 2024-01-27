$(document).ready(function(){

    function updateElementAttrs(item_element, reg, replacement){

        $(item_element).find('input').each(function(index, element){
            element.name = element.name.replace(reg, replacement)
            element.id = element.id.replace(reg, replacement)
            $(element).prev('label').attr('for', element.id)
            // $(element).closest('div').attr('id', 'div_'+element.id)
            if ($(element).is(':checkbox')){
                $(element).prop('checked', false);
                $(element).next('label').attr('for', element.id)
            }
        })
        $(item_element).find('select').each(function(index, element){
            element.name = element.name.replace(reg, replacement)
            element.id = element.id.replace(reg, replacement)
            $(element).prev('label').attr('for', element.id)
            $(element).closest('div').attr('id', 'div_'+element.id)
        })
        $(item_element).find('.delete_row').each(function(index, element){
            element.id = element.id.replace(reg, replacement)
            if ($(element).attr('data-parent-prefix')) $(element).attr('data-parent-prefix', $(element).attr('data-parent-prefix').replace(reg, replacement))
        })

    };

    function resetElementValue(item_element){
        $(item_element).find('input, select').each(function(index, element){
            if ($(element).is(':not(input[type="hidden"])')){
                $(element).val('');
            };
        })
    };

    $(document).on('click', '.add_parent_item', function(){
        var formCount = parseInt($('#id_parent-TOTAL_FORMS').val());
        var reg = new RegExp('parent-\\d')
        var replacement = 'parent-'+formCount  

        if (formCount < 1000){
            var parent_form_item = $(this).closest('.grandparent_form_container').find('.parent_formset_container .parent_form-item:first').clone()
            parent_form_item.attr('id', parent_form_item.attr('id').replace(reg, replacement))
            parent_form_item.attr('data-parent-prefix', parent_form_item.attr('data-parent-prefix').replace(reg, replacement))
            parent_form_item.find('.add_child_item').each(function(index, element){
                element.id = element.id.replace(reg, replacement)
            })
            updateElementAttrs(parent_form_item, reg,replacement)
            resetElementValue(parent_form_item)
            $(parent_form_item).appendTo($(this).closest('.grandparent_form_container').find('.parent_formset_container'))
            $('#id_parent-TOTAL_FORMS').val(formCount+1)

        }
    });

    $(document).on('click', '.delete_parent_item', function(){
         var formCount = parseInt($('#id_parent-TOTAL_FORMS').val());

         if (formCount > 1){
            var parent_container = $(this).closest('.parent_formset_container')
            $(this).closest('.parent_form-item').remove()
            var parent_items = parent_container.find('.parent_form-item')
            $('#id_parent-TOTAL_FORMS').val(parent_items.length)
            parent_items.each(function(parent_item_index, parent_item){
                var reg = new RegExp('parent-\\d')
                var replacement = 'parent-'+parent_item_index   
                updateElementAttrs(parent_item, reg,replacement)
            });
         };
    });


    $(document).on('click', '.add_child_item', function(){
        var prefix = $(this).attr('id')
        var formCount = parseInt($('#id_'+prefix+'-child-TOTAL_FORMS').val());

        if (formCount < 1000){
            var reg = new RegExp('child-\\d')
            var replacement = 'child-'+formCount
            var child_form_item = $('#id_'+prefix).find('.child_formset-container .child_form-item:last').clone()
            child_form_item.attr('id', child_form_item.attr('id').replace(reg, replacement))
            updateElementAttrs(child_form_item, reg,replacement)
            resetElementValue(child_form_item)
            $(child_form_item).appendTo($('#id_'+prefix).find('.child_formset-container'))
            $('#id_'+prefix+'-child-TOTAL_FORMS').val(formCount+1)
        }
    });


    $(document).on('click', '.delete_child_item', function(){
        var prefix = $(this).attr('id')
        var parent_prefix = $(this).attr('data-parent-prefix')
        var formCount = parseInt($('#id_'+parent_prefix+'-child-TOTAL_FORMS').val())

        if (formCount > 1){
           var child_container =  $(this).closest('.parent_form-item').find('.child_formset-container')
           $(this).closest('.child_form-item').remove()
           var child_items = child_container.find('.child_form-item')
           $('#id_'+parent_prefix+'-child-TOTAL_FORMS').val(child_items.length)
           child_items.each(function(child_item_index, child_item){
               var reg = new RegExp('child-\\d')
               var replacement = 'child-'+child_item_index   
               updateElementAttrs(child_item, reg,replacement)
           });
        };
   });

});
