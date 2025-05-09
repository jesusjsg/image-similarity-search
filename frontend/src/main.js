const form = document.getElementById('search-form')
const resultDiv = document.getElementById('result')
const fileInput = document.getElementById('image-input')

const API_BASE_URL = 'http://192.168.0.102:8000'
const API_ENDPOINT = `${API_BASE_URL}/image/upload`
console.log('API Endpoint:', API_ENDPOINT)
form.addEventListener('submit', async (e) => {
    e.preventDefault()

    if (!fileInput.files || fileInput.files.length === 0) {
        resultDiv.innerHTML = '<p style="color: orange">Por favor, selecciona una imagen.</p>'
        return
    }
  
    const file = fileInput.files[0]
    const formData = new FormData()
    formData.append('file', file)

    resultDiv.innerHTML = '<p>Buscando imágenes similares...</p>'

    try {
        const res = await fetch(API_ENDPOINT, {
            method: 'POST',
            body: formData
        })

        if (!res.ok) {
            let errorDetail = `Error: ${res.status} ${res.statusText}`
            try {
                const errorData = await res.json()
                errorDetail = errorData.detail || JSON.stringify(errorData)
            } catch (jsonError) {
                try {
                   errorDetail = await res.text()
                } catch(textError) {
                   errorDetail = `Error ${res.status}: ${res.statusText}`
                }
            }
            throw new Error(`Error del servidor: ${errorDetail}`)
        }

        const data = await res.json()
        console.log('Respuesta del servidor:', data)

        if (data.results && data.results.length > 0) {
            const resultsToShow = data.results.slice(0, 20)
            let resultsHtml = '<div style="display: flex flex-wrap: wrap gap: 15px justify-content: center">'

            resultsToShow.forEach(individualResult => {
                const imageUrl = individualResult.image_url
                const filenameStem = individualResult.name || 'N/A'
                const score = individualResult.score

                const imageTag = imageUrl && typeof imageUrl === 'string' && imageUrl.startsWith('http')
                    ? `<img src="${imageUrl}"
                           alt="Resultado: ${filenameStem}"
                           style="max-width: 200px max-height: 200px border: 1px solid #ccc border-radius: 5px object-fit: contain display: block margin: auto"
                           loading="lazy"
                           onerror="this.style.display='none' this.nextElementSibling.style.display='block' console.error('Error al cargar imagen:', this.src)">
                       <p style="color: red display: none font-size: 0.8em">Error al cargar imagen</p>`
                    : `<div style="width: 200px height: 200px border: 1px dashed #ccc display: flex align-items: center justify-content: center text-align: center font-size: 0.9em color: #555">(Imagen no disponible - URL: ${imageUrl || 'No provista'})</div>`

                resultsHtml += `
                  <div style="border: 1px solid #eee padding: 10px border-radius: 8px text-align: center width: 220px">
                    <p style="font-size: 0.9em word-wrap: break-word">${filenameStem}</p>
                    <p style="font-size: 0.8em color: #333">Score: ${score !== undefined && score !== null ? score.toFixed(4) : 'N/A'}</p>
                    ${imageTag}
                  </div>
                `
            })
            resultsHtml += '</div>'
            resultDiv.innerHTML = resultsHtml

        } else {
            resultDiv.innerHTML = '<p>No se encontraron resultados similares.</p>'
        }
    } catch (error) {
        console.error('Error durante la búsqueda:', error)
        resultDiv.innerHTML = `<p style="color: red">Hubo un error al hacer la búsqueda: ${error.message || error}</p>`
    }
})
