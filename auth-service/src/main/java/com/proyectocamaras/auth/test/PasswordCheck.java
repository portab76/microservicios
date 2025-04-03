package com.proyectocamaras.auth.test;
/*
 * Validador de Contraseñas
 * Verificar si una contraseña en texto plano coincide con su versión encriptada almacenada
 */
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

public class PasswordCheck {
    public static void main(String[] args) {
        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
        
        String rawPassword = "admin123"; // La clave que quieres probar
        String hashedPassword = "$2a$10$VXoZGAexaFqwZ3Kwz9LPQeAmXoeJ7gbyv7zJ10BrnxA0fmPb4oe9q";
        boolean matches = encoder.matches(rawPassword, hashedPassword);
        System.out.println("¿La contraseña es válida? " + matches);
    }
}
