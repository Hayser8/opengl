
from xml.dom.expatbuilder import FragmentBuilder

vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    gl_Position = projectionMatrix *viewMatrix * modelMatrix * vec4(position , 1.0); 
    outTexCoords = texCoords;
    outNormals = normals;
}

'''
#la textura solo se usa n el fragment shader
#gl_Position = modelMatrix * vec4(position + normals * sin(time * 3) / 10, 1.0); 

fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
out vec3 outNormals;

uniform sampler2D tex;

out vec4 fragColor;

void main()
{
    fragColor = texture(tex, outTexCoords);
}
'''

fat_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    gl_Position = projectionMatrix *viewMatrix * modelMatrix * vec4(position +normals * sin(time * 3) / 10 , 1.0); 
    outTexCoords = texCoords;
    outNormals = normals;
}

'''

water_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    gl_Position = projectionMatrix *viewMatrix * modelMatrix * vec4(position +vec3(0,1,0) *sin(time * position.x *10)  /10 , 1.0); 
    outTexCoords = texCoords;
    outNormals = normals;
}

'''
wave= '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    vec3 modifiedPosition = position;
    modifiedPosition.y += sin(position.x * 5.0 + time * 3.0) * 0.1; // Efecto de onda
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(modifiedPosition, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

pulse = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float scale = 1.0 + 0.2 * sin(time * 2.0);
    vec3 modifiedPosition = position * scale;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(modifiedPosition, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

color = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;
uniform float time;

out vec4 fragColor;

void main()
{
    vec4 textureColor = texture(tex, outTexCoords);
    float red = 0.5 + 0.5 * sin(time + outTexCoords.x * 10.0);
    float green = 0.5 + 0.5 * sin(time + outTexCoords.y * 10.0);
    float blue = 0.5 + 0.5 * sin(time + outTexCoords.x * 10.0 + outTexCoords.y * 10.0);
    fragColor = vec4(textureColor.rgb * vec3(red, green, blue), textureColor.a);
}

'''

metallic = '''

#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;
uniform vec3 lightPosition; // Ajusta esta posición de luz en el código
uniform float time;

out vec4 fragColor;

void main()
{
    vec4 textureColor = texture(tex, outTexCoords);
    vec3 lightDir = normalize(lightPosition - vec3(0.0, 0.0, 5.0)); // Luz en posición fija
    float diffuse = max(dot(normalize(outNormals), lightDir), 0.0);

    // Simulación de reflejo especular para un efecto metálico
    float specularStrength = 0.8;
    vec3 viewDir = normalize(-vec3(0.0, 0.0, 5.0));
    vec3 reflectDir = reflect(-lightDir, normalize(outNormals));
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 16.0);

    vec3 metalColor = mix(textureColor.rgb, vec3(0.9, 0.9, 1.0), 0.5); // Mezcla con un tono metálico suave
    vec3 finalColor = metalColor * diffuse + specularStrength * spec * vec3(1.0, 1.0, 1.0);

    fragColor = vec4(finalColor, textureColor.a);
}


'''

ripple = '''

#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float ripple = sin(length(position.xy) * 5.0 - time * 5.0) * 0.1;
    vec3 modifiedPosition = position + normals * ripple;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(modifiedPosition, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}

'''

twist = ''' 
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float twist = position.y * 0.5;
    vec3 modifiedPosition = vec3(
        position.x * cos(twist) - position.z * sin(twist),
        position.y,
        position.x * sin(twist) + position.z * cos(twist)
    );
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(modifiedPosition, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

skybox_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 inPosition;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec3 texCoords;

void main()
{
    texCoords = inPosition;
    gl_Position = projectionMatrix * viewMatrix * vec4(inPosition, 1.0);
}

'''


skybox_fragment_shader = '''
#version 450 core

uniform samplerCube skybox;

in vec3 texCoords;

out vec4 fragColor;

void main()
{
    fragColor = texture(skybox, texCoords);
}

'''