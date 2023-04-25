(function($){var settings={prependTo:'nav',switchWidth:768,topOptionText:'Select a page:'},menuCount=0,uniqueLinks=[];function goTo(url){document.location.href=url;}
function menuExists(){return($('.mnav').length)?true:false;}
function isList($this){var pass=true;$this.each(function(){if(!$(this).is('ul')&&!$(this).is('ol')){pass=false;}});return pass;}
function isMobile(){return($(document).width()<settings.switchWidth);}
function getText($item){return $.trim($item.clone().children('ul, ol').remove().end().text());}
function isUrlUnique(url){return($.inArray(url,uniqueLinks)===-1)?true:false;}
function createOption($item,$container,text){var $selected='',$disabled='',$sel_text='';if($item.hasClass('current'))$selected='selected';if($item.hasClass('disabled')){if($('.current').length)$disabled='disabled';else $disabled='selected';}
$sel_text=$.trim(getText($item));$sel_text=$sel_text.replace('»','');if($item.parent('ul ul').length)$sel_text=' – '+ $sel_text;if($item.parent('ul ul ul').length)$sel_text='– '+ $sel_text;if($item.parent('ul ul ul ul').length)$sel_text='– '+ $sel_text;if(!text){$('<option value="'+$item.find('a:first').attr('href')+'" '+ $selected+' '+ $disabled+'>'+ $sel_text+'</option>').appendTo($container);}
else{$('<option value="'+$item.find('a:first').attr('href')+'" '+ $selected+' '+ $disabled+'>'+text+'</option>').appendTo($container);}}
function createGroup($group,$container){$group.children('ul, ol').each(function(){$(this).children('li').each(function(){createOption($(this),$container);$(this).each(function(){var $li_ch=$(this),$container_ch=$container;createGroup($li_ch,$container_ch);});});});}
function createSelect($menu){var $select=$('<select id="mm'+menuCount+'" class="mnav">');menuCount++;if(settings.topOptionText){createOption($('<li class="disabled"><a href="#">'+settings.topOptionText+'</a></li>'),$select);}
$menu.children('li').each(function(){var $li=$(this);if($li.children('ul, ol').length){createOption($li,$select);createGroup($li,$select);}
else{createOption($li,$select);}});$select.change(function(){goTo($(this).val());}).prependTo(settings.prependTo);}
function runPlugin(){if(isMobile()&&!menuExists()){$menus.each(function(){createSelect($(this));});}
if(isMobile()&&menuExists()){$('.mnav').show();$menus.hide();}
if(!isMobile()&&menuExists()){$('.mnav').hide();$menus.show();}}
$.fn.mobileMenu=function(options){if(options){$.extend(settings,options);}
if(isList($(this))){$menus=$(this);runPlugin();$(window).resize(function(){runPlugin();});}else{alert('mobileMenu only works with <ul>/<ol>');}};})(jQuery);$(document).ready(function(){$('.sf-menu').mobileMenu();});