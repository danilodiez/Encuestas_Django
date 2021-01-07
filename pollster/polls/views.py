from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Question, Choice
#obtener preguntas y mostrarlas

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list':latest_question_list}
    return render(request, 'polls/index.html', context)


#mostrar preguntas especificas y elecciones
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("La pregunta no existe")
    
    return render(request, 'polls/detail.html', {'question': question })

#mostramos los resultados
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question })


#metodo para votar
def vote(request, question_id):
    
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Volvemos a mostar el formulario d ela encuesta.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "No seleccionaste una opcion.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #Siempre retorna un HttpResponseDirect despues de tratar correctamente
        # el guardado de la info.Previene a la info de guardarse 2 veces si
        # el usuario le da al boton de volver.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))